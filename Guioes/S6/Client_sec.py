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

conn_port = 8443
max_msg_size = 9999

key = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

class Client:
    """ Classe que implementa a funcionalidade de um CLIENTE. """
    
    def __init__(self, sckt=None):
        """ Construtor da classe. """
        self.sckt = sckt
        self.msg_cnt = 0

    
    def aes_gcm_enc(self, mensagem):        
        nonce = os.urandom(16)
        aesgcm = AESGCM(key.encode())

        mensagem_enc = nonce + aesgcm.encrypt(nonce, mensagem, None)

        return mensagem_enc


    def aes_gcm_dec(self, mensagem):
        nonce = mensagem[0:16]
        ciphertext_e_tag = mensagem[16:]

        aesgcm = AESGCM(key.encode())

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
        
        if len(msg)>0:
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