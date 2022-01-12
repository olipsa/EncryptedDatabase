"""Methods for executing queries on SQLite database."""
import sqlite3

con = None


def connect(db_path):
    """Create new connection with the db file provided as argument."""
    global con
    con = sqlite3.connect(db_path)


def close_connection():
    """Close current connection."""
    global con
    con.close()


def create_table():
    """Create table needed to store files."""

    global con
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS enc_files
                           (file_name text NOT NULL PRIMARY KEY, 
                           enc_algorithm text, 
                           public_key text, 
                           private_key text
                           )'''
                   )
    cursor.close()


def insert_file(file_name, algorithm, public_key, private_key):
    """Insert into table a row with file metadata.
    If the file name already exists, an error is raised.
    """

    global con
    cursor = con.cursor()
    try:
        cursor.execute(f"INSERT INTO enc_files VALUES("
                       f"'{file_name}',"
                       f"'{algorithm}',"
                       f"'{public_key}',"
                       f"'{private_key}') "
                       )
    except Exception as e:
        print(e)
        return False
    else:
        con.commit()
        return True
    finally:
        cursor.close()


def delete_file(file_name):
    """Delete specific line with metadata of file provided as argument."""
    global con
    cursor = con.cursor()
    result = cursor.execute(f"DELETE FROM enc_files WHERE file_name='{file_name}'")
    if result.rowcount > 0:
        print("File removed from db.")
        con.commit()
    else:
        print("File not stored in db.")
    cursor.close()


def get_file_keys(file_name):
    """Return a tuple (public_key, private_key) or None if the file is not found."""
    global con
    cursor = con.cursor()
    result = cursor.execute(f"SELECT public_key, private_key FROM enc_files WHERE file_name='{file_name}'")
    keys = result.fetchone()
    if keys is not None:
        cursor.close()
        return keys
    cursor.close()
    return None


def get_file_enc_algorithm(file_name):
    """Return a string containing the name of the algorithm used for encryption"""

    global con
    cursor = con.cursor()
    result = cursor.execute(f"SELECT enc_algorithm FROM enc_files WHERE file_name='{file_name}'")
    algorithm = result.fetchone()
    if algorithm is not None:
        cursor.close()
        return algorithm[0]
    cursor.close()
    return None

