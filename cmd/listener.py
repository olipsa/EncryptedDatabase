"""
Methods for checking whether a command is implemented or not.
"""
from cmd.commands import Add, Read, Delete
from database.connection import create_table, close_connection


def start():
    """Prompts the user to enter a new command in an infinite loop, until exit keyword is introduced."""
    create_table()

    while True:
        input_command = input("Input the command to be used: ").lower()
        if input_command == "add":
            command = Add()
        elif input_command == "read":
            command = Read()
        elif input_command == "delete":
            command = Delete()
        elif input_command == "exit":
            break
        else:
            print("Command not found")
            continue
        command.start()
        command.treat()

    close_connection()


