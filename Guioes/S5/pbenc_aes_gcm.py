import os
import sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # You may adjust the number of iterations as per your requirement
        backend=default_backend()
    )
    return kdf.derive(password)

def read_password():
    return input("Enter passphrase: ").encode()

def aes_gcm_enc(input_file, password):
    output_file = input_file + ".enc"
    salt = os.urandom(16)
    key = derive_key(password, salt)
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    encryptor.authenticate_additional_data(salt)  # Authenticating additional data (salt)

    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        outfile.write(salt)
        outfile.write(nonce)
        
        message = infile.read()
        ciphertext = encryptor.update(message)
        outfile.write(ciphertext)

    print(f"Encryption completed. Result saved to {output_file}")

def aes_gcm_dec(input_file, password):
    if not input_file.endswith('.enc'):
        print("Error: File is not encrypted.")
        sys.exit(1)
    
    output_file = input_file + ".dec"

    with open(input_file, 'rb') as infile:
        arquivo_bytes = infile.read()
        
        salt = arquivo_bytes[0:16]
        nonce = arquivo_bytes[16:32]
        ciphertext_e_tag = arquivo_bytes[32:]
        tag = arquivo_bytes[-16:]

        key = derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        try:
            decrypted_data = decryptor.update(ciphertext_e_tag)
            with open(output_file, 'wb') as outfile:
                outfile.write(decrypted_data)
                print(f"Decryption completed. Result saved to {output_file}")
        except ValueError:
            print("Error: Authentication tag is not valid.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pbenc_aes_gcm.py <enc|dec> <input_file>")
        sys.exit(1)

    command = sys.argv[1]
    input_file = sys.argv[2]
    password = read_password()

    if command == "enc":
        aes_gcm_enc(input_file, password)
    elif command == "dec":
        aes_gcm_dec(input_file, password)
    else:
        print("Invalid command. Please use 'enc' or 'dec'.")
        sys.exit(1)
