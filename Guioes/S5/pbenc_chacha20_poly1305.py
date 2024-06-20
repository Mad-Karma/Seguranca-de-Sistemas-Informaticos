import os
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.poly1305 import Poly1305
from cryptography.hazmat.primitives import constant_time

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

    cipher = Cipher(algorithms.ChaCha20(key[:32], nonce), mode=None, backend=default_backend())

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

        # Calculate the Poly1305 tag
        poly1305_key = key[:32]  # Use the first 32 bytes of the derived key for Poly1305
        poly1305 = Poly1305(poly1305_key)

    with open(output_file, 'rb+') as outfile:
        outfile.seek(0)
        data = outfile.read()
        poly1305.update(data)
        tag = poly1305.finalize()
        outfile.write(tag)

    print(f"Encryption completed. Result saved to {output_file}")


def chacha_dec(input_file, password):
    if not input_file.endswith('.enc'):
        print("Error: File is not encrypted.")
        sys.exit(1)

    output_file = input_file + ".dec"  # Adiciona a extensão '.dec' ao arquivo de saída

    with open(input_file, 'rb') as f:
        arquivo_bytes = f.read()
        salt = arquivo_bytes[0:16]
        nonce = arquivo_bytes[16:32]
        ciphertext = arquivo_bytes[32:-16]
        tag = arquivo_bytes[-16:]

        key = derive_key(password, salt)

        # Calculate the Poly1305 key from the derived key
        poly1305_key = key[-32:]  # Use the last 32 bytes of the derived key for Poly1305

        # Verify the Poly1305 tag
        poly1305 = Poly1305(poly1305_key)
        poly1305.update(arquivo_bytes[:-16])
        try:
            poly1305.verify(tag)
        except InvalidSignature:
            print("Error: MAC verification failed.")
            sys.exit(1)

    cipher = Cipher(algorithms.ChaCha20(key[:32], nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()

    with open(output_file, 'wb') as outfile:
        decrypted_data = decryptor.update(ciphertext)
        outfile.write(decrypted_data)

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
