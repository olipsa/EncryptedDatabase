import binascii
import os.path
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt

from db.connection import insert_file, get_file_keys, get_file_enc_algorithm


def ask_for_path():
    """Prompt user to input the path where the decrypted file should be saved.
    Internal loop: if provided path is not correct, user is informed,
    and he is asked to enter another path.
    """

    while True:
        path = input("Choose where to save file: ")
        if not path.endswith("\\"):
            path += "\\"
        if not os.path.isdir(path):
            print("Path provided is not a directory.")
            print(path)
            continue

        return path


class Algorithms:
    """Class for storing implemented encryption algorithms.
    Each one has methods to encrypt and decrypt a file.
    """

    ENCRYPTION_ALG = ['RSA', 'ECIES']
    ENCRYPTED_FOLDER = "./encrypted_files/"

    def encrypt_file(self, file_path, algorithm):
        """Call the function that encrypts the file with the provided algorithm."""

        if self.ENCRYPTION_ALG[algorithm] == 'RSA':
            self.encrypt_file_rsa(file_path)
        elif self.ENCRYPTION_ALG[algorithm] == 'ECIES':
            self.encrypt_file_ecies(file_path)
        else:
            print("Algorithm not implemented.")

    def decrypt_file(self, file_name):
        """Get the encryption algorithm used for encryption from database.
        Call the function that decrypts file with the method used for encryption.
        """

        algorithm = get_file_enc_algorithm(file_name)
        if algorithm == 'RSA':
            self.decrypt_file_rsa(file_name)
        elif algorithm == 'ECIES':
            self.decrypt_file_ecies(file_name)
        else:
            print("Unable to decrypt file. Possible reasons: file was either deleted from db, "
                  "or algorithm used for encryption is not implemented.")

    def encrypt_file_rsa(self, file_path):
        """Encrypt file provided as argument using RSA."""

        file_name = os.path.basename(file_path)
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()
        encryptor = PKCS1_OAEP.new(public_key)

        private_key_str = private_key.exportKey().decode("utf-8")
        public_key_str = public_key.exportKey().decode("utf-8")
        if not insert_file(file_name, "RSA", public_key_str, private_key_str):
            print("Unable to encrypt file.")
            return

        with open(file_path, "rb") as file:
            content = file.read()

        res = []
        max_length = 200
        for i in range(0, len(content), max_length):
            res.append(encryptor.encrypt(content[i:i+max_length]))
        ciphertext = b''.join(res)

        with open(self.ENCRYPTED_FOLDER + file_name+"_enc", "wb") as enc_file:
            enc_file.write(ciphertext)

        print("File encrypted with RSA.")

    def decrypt_file_rsa(self, file_name):
        """Decrypt file provided as argument using RSA."""

        keys = get_file_keys(file_name)
        if keys is None:
            print("File not found in db.")
            return
        public_key_str, private_key_str = keys
        retrieved_private_key = RSA.importKey(private_key_str)

        with open(self.ENCRYPTED_FOLDER + file_name+"_enc", "rb") as file:
            enc_content = file.read()

        max_length = 256
        res = []
        decryptor = PKCS1_OAEP.new(retrieved_private_key)
        for i in range(0, len(enc_content), max_length):
            res.append(decryptor.decrypt(enc_content[i:i+max_length]))
        plaintext = b''.join(res)

        path = ask_for_path()

        with open(path + file_name, "wb") as file:
            file.write(plaintext)
        os.startfile(path + file_name, 'open')

    def encrypt_file_ecies(self, file_path):
        """Encrypt file provided as argument using ECIES(Elliptic Curve Integrated Encryption Scheme)."""

        file_name = os.path.basename(file_path)
        private_key = generate_eth_key()
        private_key_hex = private_key.to_hex()
        public_key_hex = private_key.public_key.to_hex()

        if not insert_file(file_name, "ECIES", public_key_hex, private_key_hex):
            print("Unable to encrypt file.")
            return

        with open(file_path, "rb") as file:
            plaintext = file.read()

        ciphertext = encrypt(public_key_hex, plaintext)
        print("Encrypted:", binascii.hexlify(ciphertext))

        with open(self.ENCRYPTED_FOLDER + file_name+"_enc", "wb") as enc_file:
            enc_file.write(ciphertext)

        print("File encrypted with Elliptic Curve Integrated Encryption Scheme.")

    def decrypt_file_ecies(self, file_name):
        """Decrypt file provided as argument using ECIES."""

        keys = get_file_keys(file_name)
        if keys is None:
            print("File not found in db.")
            return
        public_key_hex, private_key_hex = keys

        with open(self.ENCRYPTED_FOLDER + file_name + "_enc", "rb") as file:
            enc_content = file.read()

        dec_plaintext = decrypt(private_key_hex, enc_content)

        path = ask_for_path()

        with open(path + file_name, "wb") as file:
            file.write(dec_plaintext)
        os.startfile(path + file_name, 'open')
