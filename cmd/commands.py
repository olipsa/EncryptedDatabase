class Add:
    def __init__(self, folder):
        self.file_path = None
        self.encrypted_folder = folder

    def start(self):
        while True:
            path = input("Provide the path of the file to be added or 'none' to stop command: ")
            if path.lower() == "none":
                break
            try:
                with open(path, "rb") as f:
                    content = f.read()
                    self.file_path = path
                    break
            except FileNotFoundError:
                print("Incorrect path.")
            except PermissionError:
                print("No permission to open this file.")

    def treat(self):
        if self.file_path is None:
            print("No action will be taken.")
        else:
            print("Adding file to db..")


class Read:
    def __init__(self, folder):
        self.file_name = None
        self.encrypted_folder = folder

    def start(self):
        while True:
            file = input("Provide the name of the file to be read or 'none' to stop this command: ")
            if file.lower() == "none":
                break
            try:
                f = open(self.encrypted_folder+file, "rb")
            except FileNotFoundError:
                print("File not found.")
                print("../encrypted_files/"+self.file_name)
            else:
                self.file_name = file
                break

    def treat(self):
        if self.file_name is None:
            print("No action will be taken.")
        else:
            print("Reading file from db...")


class Delete:
    def __init__(self, folder):
        self.file_name = None
        self.encrypted_folder = folder

    def start(self):
        while True:
            file = input("Provide the name of the file to be deleted or 'none' to stop this command: ")
            if file == "none":
                break
            try:
                f = open(self.encrypted_folder + file, "rb")
            except FileNotFoundError:
                print("File not found.")
            else:
                self.file_name = file
                break

    def treat(self):
        if self.file_name is None:
            print("No action will be taken.")
        else:
            print("Deleting file from db...")
