import sys
import itertools

def xor_encrypt_decrypt(ciphertext, key):
    return bytes(a ^ b for a, b in zip(ciphertext, itertools.cycle(key)))

def load_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

def decrypt_with_keywords(ciphertext, keywords):
    for key in itertools.product(*keywords):
        key_bytes = b''.join(word.encode() for word in key)
        decrypted = xor_encrypt_decrypt(ciphertext, key_bytes)
        if all(word.encode() in decrypted for word in key):
            return decrypted.decode()
    return None



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python bad_otp_attack.py <ciphertext_file> <keyword1> <keyword2> ...")
        sys.exit(1)

    ciphertext_file = sys.argv[1]
    keywords = sys.argv[2:]

    ciphertext = load_file(ciphertext_file)
    plaintext = decrypt_with_keywords(ciphertext, keywords)

    if plaintext:
        print(plaintext)
    else:
        print("Failed to decrypt the ciphertext with the provided keywords.")
