import sqlite3

con = None
cursor = None


def connect(db_path):
    global con
    con = sqlite3.connect(db_path)


def create_table():
    global con, cursor
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS enc_files
                           (file_name text NOT NULL PRIMARY KEY, 
                           enc_algorithm text, 
                           public_key text, 
                           private_key text)''')
    cursor.close()


def close_connection():
    con.close()


