# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket
import os
import sys
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
from cryptography.hazmat.primitives.asymmetric.dh import DHParameterNumbers

conn_port = 8443
max_msg_size = 9999


p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2

class Client:
    """ Classe que implementa a funcionalidade de um CLIENTE. """
    
    def __init__(self, sckt=None):
        """ Construtor da classe. """
        self.sckt = sckt
        self.msg_cnt = 0
        self.server_public_key = None
        self.peer_private_key = None
        self.shared_key = None
        self.derived_key = None

    
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

        if self.server_public_key is None and self.msg_cnt == 1:
            parameters_numbers = dh.DHParameterNumbers(p, g)
            parameters = parameters_numbers.parameters(default_backend())
            self.peer_private_key = parameters.generate_private_key()
            peer_public_key = self.peer_private_key.public_key()
            peer_public_key_serialized = peer_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

            return peer_public_key_serialized

        if self.server_public_key is None and self.msg_cnt == 2:
            self.server_public_key = load_pem_public_key(msg, backend=default_backend())
        
        if self.shared_key is None and self.msg_cnt == 2:
            self.shared_key = self.peer_private_key.exchange(self.server_public_key)

            self.derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'handshake data',
            ).derive(self.shared_key)

        
        if self.derived_key is not None and self.msg_cnt >= 2:
            if (self.msg_cnt > 2):
                mensagem_dec = self.aes_gcm_dec(msg)
                print('Received (%d): %r' % (self.msg_cnt , mensagem_dec.decode()))
        
            print('Input message to send (empty to finish)')
            new_msg = input().encode()
            
            mensagem_enc = self.aes_gcm_enc(new_msg)

            return mensagem_enc if len(new_msg)>0 else None



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