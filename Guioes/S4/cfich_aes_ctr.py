import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def generate_random_bytes(output_file):
    num_bytes = 32
    with open(output_file, 'wb') as file:
        random_bytes = os.urandom(num_bytes)
        file.write(random_bytes)

def read_key_from_file(key_file):
    with open(key_file, 'rb') as file:
        key = file.read(32)
    return key

def aes_ctr_enc(input_file, key_file, output_file):
    key = read_key_from_file(key_file)
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), mode=modes.CTR(nonce), backend=default_backend())

    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        outfile.write(nonce)
        encryptor = cipher.encryptor()
        chunk_size = 64 * 1024
        while True:
            chunk = infile.read(chunk_size)
            if len(chunk) == 0:
                break
            ciphertext = encryptor.update(chunk)
            outfile.write(ciphertext)

def aes_ctr_dec(input_file, key_file, output_file):
    key = read_key_from_file(key_file)
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        nonce = infile.read(16)
        cipher = Cipher(algorithms.AES(key), mode=modes.CTR(nonce), backend=default_backend())
        decryptor = cipher.decryptor()

        chunk_size = 64 * 1024
        while True:
            chunk = infile.read(chunk_size)
            if len(chunk) == 0:
                break
            decrypted_chunk = decryptor.update(chunk)
            outfile.write(decrypted_chunk)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cfich_aes_ctr.py <setup|enc|dec> [args]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "setup":
        if len(sys.argv) != 3:
            print("Usage: python3 cfich_aes_ctr.py setup <key_file>")
            sys.exit(1)
        key_file = sys.argv[2]
        generate_random_bytes(key_file)
        print(f"Key file '{key_file}' generated successfully.")

    elif command in ["enc", "dec"]:
        if len(sys.argv) != 4:
            print(f"Usage: python3 cfich_aes_ctr.py {command} <fich> <fkey>")
            sys.exit(1)
        fich = sys.argv[2]
        key_file = sys.argv[3]

        if command == "enc":
            fich_input = fich
            fich_output =  fich + ".enc" 
            aes_ctr_enc(fich_input, key_file, fich_output)
            print(f"CTR Encryption completed. Result saved to {fich_output}")

        elif command == "dec":
            fich_input = fich
            fich_input_enc = fich_input 
            fich_output =  fich_input_enc + ".dec"
            aes_ctr_dec(fich_input_enc, key_file, fich_output)
            print(f"CTR Decryption completed. Result saved to {fich_output}")

    else:
        print("Invalid command. Please use 'setup', 'enc', or 'dec'.")
        sys.exit(1)
