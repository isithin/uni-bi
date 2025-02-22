import mysql.connector
import time
import os

# Warte, bis MySQL verfügbar ist
time.sleep(10)

# Verbindung zu MySQL herstellen
def connect():
    try:
        db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        return db
    except Exception as e:
        print(e)
        return None

def create_table(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS example (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        )
        """
    )
 
def insert_data(cursor, db):
    cursor.execute("INSERT INTO example (name) VALUES ('MiiiTest')")
    db.commit()

def read_data(cursor):
    cursor.execute("SELECT * FROM example")
    for row in cursor.fetchall():
        print(row)

def main():
    db = connect()
    if db is not None:
        print("Connected to MySQL")
    else:
        print("Connection to MySQL failed")
    cursor = db.cursor()

    create_table(cursor)
    insert_data(cursor, db)
    read_data(cursor) # Just for debugging

    cursor.close()
    db.close()

main()
