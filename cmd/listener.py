from cmd.commands import Add, Read, Delete


def start():
    encrypted_files = "./encrypted_files/"
    while True:
        input_command = input("Input the command to be used: ").lower()
        if input_command == "add":
            command = Add(encrypted_files)
        elif input_command == "read":
            command = Read(encrypted_files)
        elif input_command == "delete":
            command = Delete(encrypted_files)
        elif input_command == "exit":
            break
        else:
            print("Command not found")
            continue
        command.start()
        command.treat()
