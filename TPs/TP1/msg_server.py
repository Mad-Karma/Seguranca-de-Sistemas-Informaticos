# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket
import os
import sys
import datetime
import time
import re

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509
from cryptography.hazmat.primitives.serialization import pkcs12

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


def cert_validsubject(cert):
    """verifica atributos do campo 'subject'. 'attrs'
    é uma lista de pares '(attr,value)' que condiciona
    os valores de 'attr' a 'value'."""

    cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    result = bool(re.search(r"SSI MSG Relay Client", cn))

    if result == False:
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
        cert_validsubject(cert)
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

def get_userdata(p12_fname):
    with open(p12_fname, "rb") as f:
        p12 = f.read()
    password = None
    (private_key, user_cert, [ca_cert]) = pkcs12.load_key_and_certificates(p12, password)
    return (private_key, user_cert, ca_cert)




class Mensagem:
    def __init__(self, sender, assunto, corpo, timestamp, assinatura, certificado):
        self.sender = sender
        self.assunto = assunto
        self.corpo = corpo
        self.timestamp = timestamp
        self.assinatura = assinatura
        self.certificado = certificado
        self.lida = 0
    
    def imprimir(self):
        print("Enviada por:", self.sender)
        print("Assunto:", self.assunto)
        print("Corpo:", self.corpo)
        print("Timestamp:", self.timestamp)


client_queues = {}

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
        self.private_key_RSA = None
        self.certificado_servidor = None
        self.certificado_CA = None
        self.certificado_peer = None

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
     
    def get_client_queue(self, client_uid):
        global client_queues
        return client_queues.get(client_uid, [])

        
    def process(self, msg):
        """ Processa uma mensagem (`bytestring`) enviada pelo CLIENTE.
            Retorna a mensagem a transmitir como resposta (`None` para
            finalizar ligação) """
        self.msg_cnt += 1 
        global client_queues

        if self.msg_cnt == 1:
            self.peer_public_key_serialized = msg
            self.peer_public_key = load_pem_public_key(msg, backend=default_backend())

            parameters_numbers = dh.DHParameterNumbers(p, g)
            parameters = parameters_numbers.parameters(default_backend())
            self.server_private_key = parameters.generate_private_key()
            self.server_public_key = self.server_private_key.public_key()
            self.server_public_key_serialized = self.server_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)


            self.private_key_RSA, self.certificado_servidor, self.certificado_CA = get_userdata("MSG_SERVER.p12")

            signature = self.private_key_RSA.sign(
                self.server_public_key_serialized + msg,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            certificado_servidor_serialized = self.certificado_servidor.public_bytes(encoding=serialization.Encoding.PEM)

            pair_key_sign = mkpair(self.server_public_key_serialized, signature)
            pair = mkpair(pair_key_sign, certificado_servidor_serialized)

            return pair
        
        if self.msg_cnt == 2:
            signature_peer, certificado_peer_serialized = unpair(msg)

            self.certificado_peer = x509.load_pem_x509_certificate(certificado_peer_serialized)

            if valida_cert(self.certificado_CA, self.certificado_peer):
                public_key_peer_RSA = self.certificado_peer.public_key()

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

        if self.msg_cnt > 2:
            mensagem_dec = self.aes_gcm_dec(msg)

            if len(mensagem_dec) == 8:
                if self.certificado_peer.subject:
                    for attr in self.certificado_peer.subject:
                        if attr.oid == x509.NameOID.PSEUDONYM:
                            uid = attr.value.strip()
                
                client_queue = self.get_client_queue(uid)

                formatted_messages = [
                    f"{index + 1}:{message.sender}:{message.timestamp}:{message.assunto}"
                    for index, message in enumerate(client_queue)
                    if message.lida == 0
                ]

                queues_string = "\n".join(formatted_messages)

                queues_serialized = queues_string.encode()

                queue_encrypted = self.aes_gcm_enc(queues_serialized)

                tempo_segundos = int(time.time())
                timestamp = datetime.datetime.fromtimestamp(tempo_segundos).strftime('%H:%M:%S')
                print(timestamp + "  " + uid + " -> askqueue")

                return queue_encrypted
                
            else:
                comando, bocado2 = unpair(mensagem_dec)
                comando = comando.decode()

                if comando == "send":
                    uid, pair_ass = unpair(bocado2)
                    uid = uid.decode()
                    assinatura, pair_subject_mensagem = unpair(pair_ass)
                    subject, mensagem = unpair(pair_subject_mensagem)
                    subject = subject.decode()
                    mensagem = mensagem.decode()

                    tempo_segundos = int(time.time())
                    timestamp = datetime.datetime.fromtimestamp(tempo_segundos).strftime('%H:%M')

                    if uid not in client_queues:
                        client_queues[uid] = []

                    if self.certificado_peer.subject:
                        for attr in self.certificado_peer.subject:
                            if attr.oid == x509.NameOID.PSEUDONYM:
                                sender_uid = attr.value.strip()

                    nova_mensagem = Mensagem(sender_uid, subject, mensagem, timestamp, assinatura, self.certificado_peer)
                    client_queues[uid].append(nova_mensagem)
                    
                    timestamp_log = datetime.datetime.fromtimestamp(tempo_segundos).strftime('%H:%M:%S')
                    print(timestamp_log + "  " + sender_uid + " -> " + comando + " " + uid + " " + subject)

                    return b'123'
                
                if comando == "getmsg":

                    num = bocado2.decode()
                    
                    if self.certificado_peer.subject:
                        for attr in self.certificado_peer.subject:
                            if attr.oid == x509.NameOID.PSEUDONYM:
                                uid = attr.value.strip()

                    client_queue = self.get_client_queue(uid)

                    num = str(int(num) - 1)
                    mensagem = client_queue[int(num)]

                    mensagem.lida = 1
                    client_queue[int(num)] = mensagem

                    formated_message = f"{mensagem.sender}:{mensagem.assunto}:{mensagem.corpo}"

                    cert_serialized = mensagem.certificado.public_bytes(encoding=serialization.Encoding.PEM)

                    pair_ass_cert = mkpair(mensagem.assinatura, cert_serialized)
                    pair_num_timestamp = mkpair(num.encode(), mensagem.timestamp.encode())
                    pair_num_timestamp_message = mkpair(pair_num_timestamp, formated_message.encode())
                    pair_geral = mkpair(pair_num_timestamp_message, pair_ass_cert)

                    mensagem_enc = self.aes_gcm_enc(pair_geral)

                    tempo_segundos = int(time.time())
                    timestamp = datetime.datetime.fromtimestamp(tempo_segundos).strftime('%H:%M:%S')
                    num = num + 1
                    print(timestamp + "  " + uid + " -> getmsg " + num)

                    return mensagem_enc

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
    # print("[%d]" % srvwrk.id)
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
