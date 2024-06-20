import sys

def decrypt_caesar(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.islower():
                if shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted < ord('A'):
                    shifted += 26
            plaintext += chr(shifted)
        else:
            plaintext += char
    return plaintext

def caesar_attack(ciphertext, words):
    for shift in range(1, 26):
        decrypted = decrypt_caesar(ciphertext, shift)
        if any(word.upper() in decrypted.upper() for word in words):
            return shift, decrypted
    return None, None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 cesar_attack.py <ciphertext> <word1> [<word2> ...]")
        sys.exit(1)

    ciphertext = sys.argv[1]
    words = sys.argv[2:]

    shift, decrypted = caesar_attack(ciphertext, words)
    if shift is None:
        print("")

    else:
        print(chr(65 + shift))
        print(decrypted)
