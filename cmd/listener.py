from cmd.commands import Add, Read, Delete
from database.connection import create_table, close_connection


def start():
    encrypted_folder = "./encrypted_files/"
    create_table()
    while True:
        input_command = input("Input the command to be used: ").lower()
        if input_command == "add":
            command = Add(encrypted_folder)
        elif input_command == "read":
            command = Read(encrypted_folder)
        elif input_command == "delete":
            command = Delete(encrypted_folder)
        elif input_command == "exit":
            break
        else:
            print("Command not found")
            continue
        command.start()
        command.treat()

    close_connection()


