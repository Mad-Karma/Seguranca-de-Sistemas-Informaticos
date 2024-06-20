import sys
import random

def bad_prng(n):
    """ an INSECURE pseudo-random number generator """
    random.seed(random.randbytes(2))
    return random.randbytes(n)

def repeat_key_to_length(key, length):
    if len(key) == 0:
        raise ValueError("Key file is empty")
    repeated_key = key * (length // len(key)) + key[:length % len(key)]
    return repeated_key

def xor_encrypt_decrypt(input_file, key_file, output_file, block_size=4096):
    with open(input_file, 'rb') as f_input, open(key_file, 'rb') as f_key, open(output_file, 'wb') as f_output:
        while True:
            input_data = f_input.read(block_size)
            f_key.seek(0)  # Move o ponteiro de leitura de volta para o início do arquivo da chave
            key_data = repeat_key_to_length(f_key.read(), len(input_data))
            if not input_data:
                break
            encrypted_data = bytes(a ^ b for a, b in zip(input_data, key_data))
            f_output.write(encrypted_data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bad_otp.py <setup|enc|dec> [args]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "setup":
        if len(sys.argv) != 4:
            print("Usage: python bad_otp.py setup <num_bytes> <key_file>")
            sys.exit(1)
        num_bytes = int(sys.argv[2])
        key_file = sys.argv[3]
        with open(key_file, 'wb') as file:
            key_bytes = bad_prng(num_bytes)
            file.write(key_bytes)
        print(f"{num_bytes} random bytes generated and saved to {key_file}")

    elif command == "enc" or command == "dec":
        if len(sys.argv) != 4:
            print(f"Usage: python bad_otp.py {command} <input_file> <key_file>")
            sys.exit(1)
        input_file = sys.argv[2]
        key_file = sys.argv[3]
        if len(key_file) == 0:
            print("Error: Key file is empty")
            sys.exit(1)
        output_file = input_file + (".enc" if command == "enc" else ".dec")
        xor_encrypt_decrypt(input_file, key_file, output_file)
        print(f"{command.capitalize()}ryption completed. Result saved to {output_file}")

    else:
        print("Invalid command. Please use 'setup', 'enc', or 'dec'.")
        sys.exit(1)
