"""Implement classes for supported commands."""
import os.path
from db.connection import delete_file
from security.encryption import Algorithms

class_ = Algorithms()


class Add:
    """Class used to encrypt a file provided from standard input."""

    def __init__(self):
        """Initialize variables used to store user input."""

        self.file_path = None
        self.input_alg = None

    def start(self):
        """Prompt user to provide the path of the file to encrypt and encryption algorithm."""

        self._input_path()
        if self.file_path is not None:
            self._input_algorithm()

    def _input_path(self):
        """Prompt user to provide the path of the file until 'none' keyword is given."""

        while True:
            path = input("Provide the path of the file to be added or 'none' to stop command: ")
            if path.lower() == "none":
                return False
            elif not os.path.exists(path):
                print("Incorrect path.")
            elif os.path.isdir(path):
                print("Unable to encrypt entire directory.")
            elif os.path.exists(class_.ENCRYPTED_FOLDER + os.path.basename(path) + "_enc"):
                print("File with same name already encrypted.")
            else:
                self.file_path = path
                return True

    def _input_algorithm(self):
        """Prompt user to provide the encryption algorithm until 'none' keyword is given."""

        while self.input_alg is None:
            for i in range(len(class_.ENCRYPTION_ALG)):
                print(str(i+1) + ". " + class_.ENCRYPTION_ALG[i])

            alg_index = input("Choose the encryption algorithm to be used: ")
            if alg_index == "none":
                break

            try:
                alg_index = int(alg_index)
            except ValueError:
                print("Invalid number provided.")
                continue
            if alg_index < 1 or alg_index > len(class_.ENCRYPTION_ALG):
                print("Invalid number provided.")
                continue

            self.input_alg = alg_index - 1

    def treat(self):
        """Use the input provided by user to add file to database for encryption."""

        if self.file_path is None or self.input_alg is None:
            print("No action will be taken.")
        else:
            print("Encrypting file...")
            class_.encrypt_file(self.file_path, self.input_alg)


class Read:
    """Class used to decrypt a file provided from standard input and open it."""

    def __init__(self):
        self.file_name = None

    def start(self):
        """Prompt user to provide the file name to read from database"""

        while True:
            file = input("Provide the name of the file to be read or 'none' to stop this command: ")
            if file.lower() == "none":
                break
            if not os.path.exists(class_.ENCRYPTED_FOLDER + file + "_enc"):
                print("File not found.")
            else:
                self.file_name = file
                break

    def treat(self):
        """Use the input provided by user to read file from database."""

        if self.file_name is None:
            print("No action will be taken.")
        else:
            class_.decrypt_file_rsa(self.file_name)


class Delete:
    """Class used to delete a file locally and from the database."""

    def __init__(self):
        self.file_name = None

    def start(self):
        """Prompt user to provide the file name to read from database"""

        file = input("Provide the name of the file to be deleted or 'none' to stop this command: ")
        if file.lower() == "none":
            return
        self.file_name = file

    def treat(self):
        """Delete provided file from database."""

        if self.file_name is None:
            print("No action will be taken.")
        else:
            if os.path.exists(class_.ENCRYPTED_FOLDER + self.file_name + "_enc"):
                os.remove(class_.ENCRYPTED_FOLDER + self.file_name + "_enc")
                print("File removed locally.")
            delete_file(self.file_name)
