from cmd import listener
from database.connection import connect

if __name__ == '__main__':

    connect('./files.db')
    listener.start()



