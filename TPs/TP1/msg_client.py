# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket
import sys
import socket
import os
import datetime
import re

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key

conn_port = 8443
max_msg_size = 9999

p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2


def get_userdata(p12_fname):
    with open(p12_fname, "rb") as f:
        p12 = f.read()
    password = None
    (private_key, user_cert, [ca_cert]) = pkcs12.load_key_and_certificates(p12, password)
    return (private_key, user_cert, ca_cert)


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


def cert_validtime(cert, now=None):
    """valida que 'now' se encontra no período
    de validade do certificado."""
    if now is None:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
    if now < cert.not_valid_before_utc or now > cert.not_valid_after_utc:
        raise x509.verification.VerificationError(
            "Certificate is not valid at this time"
        )


def cert_validsubject(cert, ent):
    """verifica atributos do campo 'subject'. 'attrs'
    é uma lista de pares '(attr,value)' que condiciona
    os valores de 'attr' a 'value'."""

    if ent == "MSG_SERVER":
        cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        result = bool(re.search(r"SSI Message Relay Server", cn))
    else:
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
    if cert.subject:
        for attr in cert.subject:
            if attr.oid == x509.NameOID.PSEUDONYM:
                sender_uid = attr.value.strip()

    if sender_uid == "MSG_SERVER":
        try:
            cert.verify_directly_issued_by(ca_cert)
            cert_validtime(cert)
            cert_validsubject(cert, sender_uid)
            cert_validexts(
                cert,[(
                        x509.ExtensionOID.EXTENDED_KEY_USAGE,
                        lambda e: x509.oid.ExtendedKeyUsageOID.SERVER_AUTH in e,
                    )],
            )
            return True
        except:
            print("Server certificate is invalid!")
            return False
    
    else:
        try:
            cert.verify_directly_issued_by(ca_cert)
            cert_validtime(cert)
            cert_validsubject(cert, sender_uid)
            cert_validexts(
                cert,[(
                        x509.ExtensionOID.EXTENDED_KEY_USAGE,
                        lambda e: x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH in e,
                    )],
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




class Client:
    """ Classe que implementa a funcionalidade de um CLIENTE. """
    def __init__(self, sckt=None):
        """ Construtor da classe. """
        self.sckt = sckt
        self.msg_cnt = 0
        self.ficheiro = None
        self.private_key_RSA = None
        self.certificado_cliente = None
        self.certificado_CA = None
        self.check_user = 0
        self.server_public_key = None
        self.peer_private_key = None
        self.shared_key = None
        self.derived_key = None
        self.peer_public_key = None
        self.peer_public_key_serialized = None
        self.check_done = 0
        self.sent = 0
        self.indice = 1


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


    def process(self, msg=b""):
        """ Processa uma mensagem (`bytestring`) enviada pelo SERVIDOR.
            Retorna a mensagem a transmitir como resposta (`None` para
            finalizar ligação) """
        
        self.msg_cnt +=1

        if len(sys.argv) == 1:
            sys.stderr.write("MSG RELAY SERVICE: command error!\n\n")
            sys.stderr.flush()

            print("Usage: python3 msg_client.py [-user <FNAME>] <command>")
            print("Commands:")
            print("  -user <FNAME>                 Specify the user data file")
            print("  send <UID> <SUBJECT>          Send a message to the user with the specified UID")
            print("  askqueue                      Request the server to send the list of unread messages")
            print("  getmsg <NUM>                  Request the server to send the message with the specified number from the queue")
            print("  help                          Display usage instructions")
            
            return None
        
        # comando: -user <FNAME>
        if sys.argv[1] == "-user":
            self.ficheiro = sys.argv[2]
            self.private_key_RSA, self.certificado_cliente, self.certificado_CA = get_userdata(self.ficheiro)
            self.check_user = 1
        else:
            self.ficheiro = "userdata.p12"
            self.private_key_RSA, self.certificado_cliente, self.certificado_CA = get_userdata(self.ficheiro)

        # Fazer o protocolo station to station
        if self.msg_cnt == 1:
            parameters_numbers = dh.DHParameterNumbers(p, g)
            parameters = parameters_numbers.parameters(default_backend())
            self.peer_private_key = parameters.generate_private_key()
            self.peer_public_key = self.peer_private_key.public_key()
            self.peer_public_key_serialized = self.peer_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

            return self.peer_public_key_serialized

        
        if self.msg_cnt == 2:
            pair, certificado_server_serialized = unpair(msg)
            server_public_key_serialized, signature = unpair(pair)

            certificado_server = x509.load_pem_x509_certificate(certificado_server_serialized)

            if valida_cert(self.certificado_CA, certificado_server):
                public_key_server_RSA = certificado_server.public_key()

                public_key_server_RSA.verify(
                    signature,
                    server_public_key_serialized + self.peer_public_key_serialized,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )

                self.server_public_key = load_pem_public_key(server_public_key_serialized, backend=default_backend())

                self.shared_key = self.peer_private_key.exchange(self.server_public_key)

                self.derived_key = HKDF(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=None,
                    info=b'handshake data',
                ).derive(self.shared_key)

            signature_peer = self.private_key_RSA.sign(
                self.peer_public_key_serialized + server_public_key_serialized,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            certificado_peer_serialized = self.certificado_cliente.public_bytes(encoding=serialization.Encoding.PEM)

            return_pair = mkpair(signature_peer, certificado_peer_serialized)

            return return_pair
    
        if self.check_done == 0:
            if sys.argv[self.indice] is None:
                self.check_done = 1

            start_index = 3 if self.check_user == 1 else 1
            
            for i, arg in enumerate(sys.argv[start_index:], start=start_index):
                if arg == "-user":
                    sys.stderr.write("MSG RELAY SERVICE: command error!\n")
                    return None

                # comando: send <UID> <SUBJECT>
                if arg == "send":
                    if self.sent == 0:
                        self.sent = 1

                        uid = sys.argv[i+1]
                        subject = sys.argv[i+2]

                        i = i + 2

                        mensagem = input()
                        if len(mensagem) > 1000:
                            sys.stderr.write("\nMSG RELAY SERVICE: message too long! Maximum allowed size is 1000 bytes.\n")
                            return None
                        
                        if self.certificado_cliente.subject:
                            for attr in self.certificado_cliente.subject:
                                if attr.oid == x509.NameOID.PSEUDONYM:
                                    uid_sender = attr.value.strip()

                        formated_message = f"{uid_sender}:{subject}:{mensagem}"
                        formated_message = formated_message.encode()

                        
                        signature = self.private_key_RSA.sign(
                            formated_message,
                            padding.PSS(
                                mgf=padding.MGF1(hashes.SHA256()),
                                salt_length=padding.PSS.MAX_LENGTH
                            ),
                            hashes.SHA256()
                        )

                        pair_subject_mensagem = mkpair(subject.encode(), mensagem.encode())
                        pair_ass = mkpair(signature, pair_subject_mensagem)
                        pair_uid = mkpair(uid.encode(), pair_ass)
                        pair_geral = mkpair(arg.encode(), pair_uid)

                        mensagem_enc = self.aes_gcm_enc(pair_geral)

                        return mensagem_enc
                    
                    else:
                        uid = sys.argv[i+1]
                        print("\nMessage sent successfully to " + uid + "!\n")  

                        return None
            
                # comando: askqueue
                if arg == "askqueue":
                    if self.sent == 0:
                        self.sent = 1
                        i = i - 1

                        argumento = arg.encode()
                        argumento_enc = self.aes_gcm_enc(argumento)

                        return argumento_enc
                    
                    else:
                        msg_decripted = self.aes_gcm_dec(msg)

                        messages_string = msg_decripted.decode()

                        print("\n")
                        print(messages_string)
                        print("\n")
                        
                        return None

                # comando: getmsg <NUM>
                if arg == "getmsg":
                    if self.sent == 0:
                        self.sent = 1
                        num = sys.argv[i + 1]

                        i = i + 1

                        pair = mkpair(arg.encode(), num.encode())
                        mensagem_enc = self.aes_gcm_enc(pair)

                        return mensagem_enc

                    else:
                        msg_decripted = self.aes_gcm_dec(msg)

                        pair_num_timestamp_message, pair_ass_cert = unpair(msg_decripted)
                        pair_num_timestamp, formated_message_encoded = unpair(pair_num_timestamp_message)
                        num, timestamp = unpair(pair_num_timestamp)
                        num = num.decode()
                        timestamp = timestamp.decode()
                        
                        formated_message = formated_message_encoded.decode()

                        assinatura, certificado_serialized = unpair(pair_ass_cert)
                        certificado = x509.load_pem_x509_certificate(certificado_serialized)

                        if valida_cert(self.certificado_CA, certificado):
                            public_key_RSA = certificado.public_key()

                            public_key_RSA.verify(
                                assinatura,
                                formated_message_encoded,
                                padding.PSS(
                                    mgf=padding.MGF1(hashes.SHA256()),
                                    salt_length=padding.PSS.MAX_LENGTH
                                ),
                                hashes.SHA256()
                            )

                            sender, assunto, corpo = formated_message.split(':')

                            print("\nReceived from:", sender)
                            print(timestamp)
                            print("\nSubject:", assunto)
                            print("\n" + corpo + "\n")

                            return None
                        
                        return None



                # comando:help
                if arg == "help":
                    print("Usage: python3 msg_client.py [-user <FNAME>] <command>")
                    print("Commands:")
                    print("  -user <FNAME>                 Specify the user data file")
                    print("  send <UID> <SUBJECT>          Send a message to the user with the specified UID")
                    print("  askqueue                      Request the server to send the list of unread messages")
                    print("  getmsg <NUM>                  Request the server to send the message with the specified number from the queue")
                    print("  help                          Display usage instructions")
                    return None
                else:
                    sys.stderr.write("MSG RELAY SERVICE: command error!\n\n")
                    sys.stderr.flush()

                    print("Usage: python3 msg_client.py [-user <FNAME>] <command>")
                    print("Commands:")
                    print("  -user <FNAME>                 Specify the user data file")
                    print("  send <UID> <SUBJECT>          Send a message to the user with the specified UID")
                    print("  askqueue                      Request the server to send the list of unread messages")
                    print("  getmsg <NUM>                  Request the server to send the message with the specified number from the queue")
                    print("  help                          Display usage instructions")
                    return None

                self.indice = i


        if self.msg_cnt > 2:
            msg_decripted = self.aes_gcm_dec(msg)

            if(msg_decripted.decode() == "done"):
                sys.exit(0)



#
#
# Funcionalidade Cliente/Servidor
#
# obs: não deverá ser necessário alterar o que se segue
#


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', conn_port)
    addr = writer.get_extra_info('peername')
    client = Client(addr)
    msg = client.process()
    while msg:
        writer.write(msg)
        msg = await reader.read(max_msg_size)
        if msg :
            msg = client.process(msg)
        else:
            break
    writer.write(b'\n')
    print('Socket closed!')
    writer.close()

def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client())


run_client()
