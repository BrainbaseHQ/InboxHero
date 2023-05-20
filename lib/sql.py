import sqlite3
from sqlite3 import Error

def create_database(db_name):
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def insert_into_database(db_name, emails):
    try:
        conn = sqlite3.connect(db_name)

        cursor = conn.cursor()

        # create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS emails
                        (id text PRIMARY KEY, from_ text, summary text, urgent integer, needs_response integer )''')
        
        # insert emails
        for email in emails:
            cursor.execute(f'''INSERT INTO emails VALUES ({email["id"]}, "{email['from'].replace('"', '')}", "{email['summary'].replace('"', '')}", {email['urgent']}, {email['needs_response']})''')

        conn.commit()

        # close connection
        cursor.close()
    except Error as e:
        print("Error: " , e)
    finally:
        if conn:
            conn.close()

def check_if_id_exists(db_name, email_id):
    try:
        conn = sqlite3.connect(db_name)

        cursor = conn.cursor()

        # create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS emails
                        (id text PRIMARY KEY, from_ text, summary text, urgent integer, needs_response integer )''')
        
        # insert emails
        cursor.execute(f'SELECT * FROM emails WHERE id = {email_id.decode("utf-8")}')
        result = cursor.fetchone()

        # close connection
        cursor.close()

        return result
    except Error as e:
        print("Error: " , e)
        return None
    finally:
        if conn:
            conn.close()