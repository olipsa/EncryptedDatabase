from cmd import listener
from db.connection import connect

if __name__ == '__main__':

    connect('db/files.db')
    listener.start()



