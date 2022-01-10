import os.path
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

from db.connection import insert_file, get_file_keys


class Algorithms:
    """Class for storing implemented encryption algorithms.
    Each one has methods to encrypt and decrypt a file.
    """

    ENCRYPTION_ALG = ['RSA']
    ENCRYPTED_FOLDER = "./encrypted_files/"

    def encrypt_file(self, file_path, algorithm):
        """Call the function that encrypts the file with the provided algorithm"""

        if self.ENCRYPTION_ALG[algorithm] == 'RSA':
            self.encrypt_file_rsa(file_path)
        else:
            print("Algorithm not implemented.")

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

        print("File encrypted.")

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

        path = input("Choose where to save file: ")

        with open(path + file_name, "wb") as file:
            file.write(plaintext)
        os.startfile(path + file_name, 'open')

