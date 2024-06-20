# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket
import os
import sys
import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa

conn_cnt = 0
conn_port = 8443
max_msg_size = 9999

p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2


def cert_validtime(cert, now=None):
    """valida que 'now' se encontra no período
    de validade do certificado."""
    if now is None:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
    if now < cert.not_valid_before_utc or now > cert.not_valid_after_utc:
        raise x509.verification.VerificationError(
            "Certificate is not valid at this time"
        )


def cert_validsubject(cert, attrs=[]):
    """verifica atributos do campo 'subject'. 'attrs'
    é uma lista de pares '(attr,value)' que condiciona
    os valores de 'attr' a 'value'."""
    # print(cert.subject)
    for attr in attrs:
        if cert.subject.get_attributes_for_oid(attr[0])[0].value != attr[1]:
            raise x509.verification.VerificationError(
                "Certificate subject does not match expected value"
            )


def cert_validexts(cert, policy=[]):
    """valida extensões do certificado.
    'policy' é uma lista de pares '(ext,pred)' onde 'ext' é o OID de uma extensão e 'pred'
    o predicado responsável por verificar o conteúdo dessa extensão."""
    for check in policy:
        ext = cert.extensions.get_extension_for_oid(check[0]).value
        if not check[1](ext):
            raise x509.verification.VerificationError(
                "Certificate extensions does not match expected value"
            )

def valida_cert(ca_cert, cert):
    try:
        cert.verify_directly_issued_by(ca_cert)
        cert_validtime(cert)
        cert_validsubject(cert, [(x509.NameOID.COMMON_NAME, "User 1 (SSI MSG Relay Client 1)")])
        cert_validexts(
            cert,
            [
                (
                    x509.ExtensionOID.EXTENDED_KEY_USAGE,
                    lambda e: x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH in e,
                )
            ],
        )
        return True
    except:
        print("Client certificate is invalid!")
        return False
    
def cert_load(fname):
        """lê certificado de ficheiro"""
        with open(fname, "rb") as fcert:
            cert = x509.load_pem_x509_certificate(fcert.read())
        return cert
    
def mkpair(x, y):
    """produz uma byte-string contendo o tuplo '(x,y)' ('x' e 'y' são byte-strings)"""
    len_x = len(x)
    len_x_bytes = len_x.to_bytes(2, "little")
    return len_x_bytes + x + y

def unpair(xy):
    """extrai componentes de um par codificado com 'mkpair'"""
    len_x = int.from_bytes(xy[:2], "little")
    x = xy[2 : len_x + 2]
    y = xy[len_x + 2 :]
    return x, y


class ServerWorker(object):
    """ Classe que implementa a funcionalidade do SERVIDOR. """
    def __init__(self, cnt, addr=None):
        """ Construtor da classe. """
        self.id = cnt
        self.addr = addr
        self.msg_cnt = 0
        self.peer_public_key = None
        self.server_private_key = None
        self.shared_key = None
        self.derived_key = None
        self.peer_public_key_serialized = None
        self.server_public_key_serialized = None
        self.server_public_key = None


    def aes_gcm_enc(self, mensagem):        
        nonce = os.urandom(16)
        aesgcm = AESGCM(self.derived_key)

        mensagem_enc = nonce + aesgcm.encrypt(nonce, mensagem, None)

        return mensagem_enc

    def aes_gcm_dec(self, mensagem):
        nonce = mensagem[0:16]
        ciphertext_e_tag = mensagem[16:]

        aesgcm = AESGCM(self.derived_key)

        try:
            decrypted_data = aesgcm.decrypt(nonce, ciphertext_e_tag, None)
            return decrypted_data
        except ValueError:
            print("Error: Authentication tag is not valid.")

    





    def process(self, msg):
        """ Processa uma mensagem (`bytestring`) enviada pelo CLIENTE.
            Retorna a mensagem a transmitir como resposta (`None` para
            finalizar ligação) """
        
        self.msg_cnt += 1

        if self.msg_cnt == 1:
            self.peer_public_key_serialized = msg
            self.peer_public_key = load_pem_public_key(msg, backend=default_backend())

            parameters_numbers = dh.DHParameterNumbers(p, g)
            parameters = parameters_numbers.parameters(default_backend())
            self.server_private_key = parameters.generate_private_key()
            self.server_public_key = self.server_private_key.public_key()
            self.server_public_key_serialized = self.server_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)


            with open("MSG_SERVER.key", "rb") as key_file:
                private_key_RSA = serialization.load_pem_private_key(
                    key_file.read(),
                    password=b'1234',
                )

            signature = private_key_RSA.sign(
                self.server_public_key_serialized + msg,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            certificado = cert_load("MSG_SERVER.crt")
            certificado_serialized = certificado.public_bytes(encoding=serialization.Encoding.PEM)

            pair_key_sign = mkpair(self.server_public_key_serialized, signature)

            pair = mkpair(pair_key_sign, certificado_serialized)

            return pair
        
        if self.msg_cnt == 2:
            signature_peer, certificado_peer_serialized = unpair(msg)

            certificado_peer = x509.load_pem_x509_certificate(certificado_peer_serialized)

            certificado_CA = cert_load("MSG_CA.crt")

            if valida_cert(certificado_CA, certificado_peer):
                public_key_peer_RSA = certificado_peer.public_key()

                public_key_peer_RSA.verify(
                    signature_peer,
                    self.peer_public_key_serialized + self.server_public_key_serialized,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )

                self.shared_key = self.server_private_key.exchange(self.peer_public_key)

                self.derived_key = HKDF(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=None,
                    info=b'handshake data',
                ).derive(self.shared_key)

            return b'123'

            

        if self.derived_key is not None and self.msg_cnt > 2:
            if self.msg_cnt > 1:            
                mensagem_dec = self.aes_gcm_dec(msg)
                
                print('%d : %r' % (self.id, mensagem_dec.decode()))
                new_msg = mensagem_dec.upper()
                
                mensagem_enc = self.aes_gcm_enc(new_msg)

                return mensagem_enc if len(new_msg)>0 else None


#
#
# Funcionalidade Cliente/Servidor
#
# obs: não deverá ser necessário alterar o que se segue
#


async def handle_echo(reader, writer):
    global conn_cnt
    conn_cnt +=1
    addr = writer.get_extra_info('peername')
    srvwrk = ServerWorker(conn_cnt, addr)
    data = await reader.read(max_msg_size)
    while True:
        if not data: continue
        if data[:1]==b'\n': break
        data = srvwrk.process(data)
        if not data: break
        writer.write(data)
        await writer.drain()
        data = await reader.read(max_msg_size)
    print("[%d]" % srvwrk.id)
    writer.close()


def run_server():
    loop = asyncio.new_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', conn_port)
    server = loop.run_until_complete(coro)
    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    print('  (type ^C to finish)\n')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    print('\nFINISHED!')

run_server()