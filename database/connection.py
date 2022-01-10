import os
import sqlite3


con = None


def connect(db_path):
    global con
    con = sqlite3.connect(db_path)


def close_connection():
    global con
    con.close()


def create_table():
    global con
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS enc_files
                           (file_name text NOT NULL PRIMARY KEY, 
                           enc_algorithm text, 
                           public_key text, 
                           private_key text)''')
    cursor.close()


def insert_file(file_name, algorithm, public_key, private_key):
    global con
    cursor = con.cursor()
    try:
        cursor.execute(f"INSERT INTO enc_files VALUES('{file_name}','{algorithm}', '{public_key}','{private_key}') ")
    except Exception as e:
        print(e)
        return False
    else:
        con.commit()
        return True
    finally:
        cursor.close()


def find_file(file_name):
    global con
    cursor = con.cursor()
    result = cursor.execute(f"SELECT * FROM enc_files WHERE file_name='{file_name}'")
    if result.fetchone() is not None:
        cursor.close()
        return True
    cursor.close()
    return False


def delete_file(file_name):
    global con
    cursor = con.cursor()
    result = cursor.execute(f"DELETE FROM enc_files WHERE file_name='{file_name}'")
    if result.rowcount > 0:
        print("File removed from db.")
        con.commit()
    else:
        print("File not stored in db.")
    cursor.close()



