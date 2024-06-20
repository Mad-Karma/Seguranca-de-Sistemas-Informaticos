import os
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # You may adjust the number of iterations as per your requirement
        backend=default_backend()
    )
    return kdf.derive(password)

def generate_random_bytes(output_file):
    num_bytes = 16
    with open(output_file, 'wb') as file:
        random_bytes = os.urandom(num_bytes)
        file.write(random_bytes)

def read_password():
    return input("Enter passphrase: ").encode()

def chacha_enc(input_file, password):
    output_file = input_file + ".enc"
    salt = os.urandom(16)
    key = derive_key(password, salt)
    nonce = os.urandom(16)  # Using 16 bytes nonce
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())

    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        outfile.write(salt)
        outfile.write(nonce)
        encryptor = cipher.encryptor()
        chunk_size = 64 * 1024
        while True:
            chunk = infile.read(chunk_size)
            if len(chunk) == 0:
                break
            ciphertext = encryptor.update(chunk)
            outfile.write(ciphertext)

    print(f"Encryption completed. Result saved to {output_file}")

def chacha_dec(input_file, password):
    if not input_file.endswith('.enc'):
        print("Error: File is not encrypted.")
        sys.exit(1)
    
    output_file = input_file + ".dec"
    
    with open(input_file, 'rb') as infile:
        salt = infile.read(16)
        nonce = infile.read(16)
        key = derive_key(password, salt)
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        chunk_size = 64 * 1024
        with open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                decrypted_chunk = decryptor.update(chunk)
                outfile.write(decrypted_chunk)

    print(f"Decryption completed. Result saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pbenc_chacha20.py <enc|dec> <input_file>")
        sys.exit(1)

    command = sys.argv[1]
    input_file = sys.argv[2]
    password = read_password()

    if command == "enc":
        chacha_enc(input_file, password)
    elif command == "dec":
        chacha_dec(input_file, password)
    else:
        print("Invalid command. Please use 'enc' or 'dec'.")
        sys.exit(1)
