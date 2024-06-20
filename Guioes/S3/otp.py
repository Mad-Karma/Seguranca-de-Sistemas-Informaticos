import sys
import os

def generate_random_bytes(num_bytes, output_file):
    with open(output_file, 'wb') as file:
        random_bytes = os.urandom(num_bytes)
        file.write(random_bytes)

def repeat_key_to_length(key, length):
    if len(key) == 0:
        raise ValueError("Key file is empty")
    repeated_key = key * (length // len(key)) + key[:length % len(key)]
    return repeated_key

def xor_encrypt_decrypt(input_file, key_file, output_file, block_size=4096):
    with open(input_file, 'rb') as f_input, open(key_file, 'rb') as f_key, open(output_file, 'wb') as f_output:
        while True:
            input_data = f_input.read(block_size)
            f_key.seek(0)  # Reset the file pointer to the beginning
            key_data = repeat_key_to_length(f_key.read(), len(input_data))
            if not input_data:
                break
            encrypted_data = bytes(a ^ b for a, b in zip(input_data, key_data))
            f_output.write(encrypted_data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python otp.py <setup|enc|dec> [args]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "setup":
        if len(sys.argv) != 4:
            print("Usage: python otp.py setup <num_bytes> <key_file>")
            sys.exit(1)
        num_bytes = int(sys.argv[2])
        key_file = sys.argv[3]
        generate_random_bytes(num_bytes, key_file)
        print(f"{num_bytes} random bytes generated and saved to {key_file}")

    elif command == "enc" or command == "dec":
        if len(sys.argv) != 4:
            print(f"Usage: python otp.py {command} <input_file> <key_file>")
            sys.exit(1)
        input_file = sys.argv[2]
        key_file = sys.argv[3]
        if os.path.getsize(key_file) == 0:
            print("Error: Key file is empty")
            sys.exit(1)
        output_file = input_file + (".enc" if command == "enc" else ".dec")
        xor_encrypt_decrypt(input_file, key_file, output_file)
        print(f"{command.capitalize()}ryption completed. Result saved to {output_file}")

    else:
        print("Invalid command. Please use 'setup', 'enc', or 'dec'.")
        sys.exit(1)
