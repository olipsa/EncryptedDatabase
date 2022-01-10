"""Actual implementation of supported commands. """
import os.path
from database.connection import find_file, delete_file
from security.encryption import Algorithms

alg_class = Algorithms()


class Add:
    def __init__(self):
        self.file_path = None
        self.input_alg = None

    def start(self):
        self._input_path()
        if self.file_path is not None:
            self._input_algorithm()

    def _input_path(self):
        while True:
            path = input("Provide the path of the file to be added or 'none' to stop command: ")
            if path.lower() == "none":
                return False
            elif not os.path.exists(path):
                print("Incorrect path.")
            elif os.path.isdir(path):
                print("Unable to encrypt entire directory.")
            elif os.path.exists(alg_class.ENCRYPTED_FOLDER+os.path.basename(path)+"_enc"):
                print("File with same name already encrypted.")
            else:
                self.file_path = path
                return True

    def _input_algorithm(self):
        while self.input_alg is None:
            for i in range(len(alg_class.ENCRYPTION_ALG)):
                print(str(i+1)+". "+alg_class.ENCRYPTION_ALG[i])

            alg_index = input("Choose the encryption algorithm to be used: ")

            try:
                alg_index = int(alg_index)
            except ValueError:
                print("Invalid number provided.")
                continue
            if alg_index < 1 or alg_index > len(alg_class.ENCRYPTION_ALG):
                print("Invalid number provided.")
                continue
            self.input_alg = alg_index - 1

    def treat(self):
        if self.file_path is None or self.input_alg is None:
            print("No action will be taken.")
        else:
            print("Encrypting file...")
            alg_class.encrypt_file(self.file_path, self.input_alg)


class Read:
    def __init__(self):
        self.file_name = None

    def start(self):
        while True:
            file = input("Provide the name of the file to be read or 'none' to stop this command: ")
            if file.lower() == "none":
                break
            try:
                f = open(alg_class.ENCRYPTED_FOLDER + file, "rb")
            except FileNotFoundError:
                print("File not found.")
            else:
                self.file_name = file
                break

    def treat(self):
        if self.file_name is None:
            print("No action will be taken.")
        else:
            print("Reading file from db...")


class Delete:
    def __init__(self):
        self.file_name = None

    def start(self):
        file = input("Provide the name of the file to be deleted or 'none' to stop this command: ")
        if file.lower() == "none":
            return
        self.file_name = file

    def treat(self):
        if self.file_name is None:
            print("No action will be taken.")
        else:
            if os.path.exists(alg_class.ENCRYPTED_FOLDER+self.file_name+"_enc"):
                os.remove(alg_class.ENCRYPTED_FOLDER+self.file_name+"_enc")
                print("File removed locally.")
            delete_file(self.file_name)
