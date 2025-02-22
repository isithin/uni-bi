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
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Bezirk (
            Name                 VARCHAR(50) NOT NULL,
            Durchschnittsalter   DECIMAL(4,1), 
            Durchschnittseinkommen DECIMAL(10,2),
            Schulabschluss       VARCHAR(50),
            Migrationsrate       DECIMAL(5,2),
            Kriminalitaetsrate   DECIMAL(5,2),
            Parkplatz_pro_Kopf   DECIMAL(5,2),
            PRIMARY KEY (Name)
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Postleitgebiet (
            Postleitzahl         VARCHAR(10) NOT NULL,
            FK_Bezirksname       VARCHAR(50) NOT NULL,
            PRIMARY KEY (Postleitzahl),
            FOREIGN KEY (FK_Bezirksname) REFERENCES Bezirk(Name)
              ON UPDATE CASCADE 
              ON DELETE RESTRICT
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Immobilie (
            ID                   INT NOT NULL,
            FK_Postleitzahl      VARCHAR(10) NOT NULL,
            Preis_warm           DECIMAL(10,2),
            Groesse              INT,
            Parkplaetze          INT,
            PRIMARY KEY (ID),
            FOREIGN KEY (FK_Postleitzahl) REFERENCES Postleitgebiet(Postleitzahl)
              ON UPDATE CASCADE
              ON DELETE CASCADE
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Supermarkt (
            ID                   INT NOT NULL,
            FK_Postleitzahl      VARCHAR(10) NOT NULL,
            Name                 VARCHAR(100),
            Discounter           BOOLEAN,          
            PRIMARY KEY (ID),
            FOREIGN KEY (FK_Postleitzahl) REFERENCES Postleitgebiet(Postleitzahl)
              ON UPDATE CASCADE
              ON DELETE CASCADE
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Haltestelle (
            ID                   INT NOT NULL,
            FK_Postleitzahl      VARCHAR(10) NOT NULL,
            Transportmittel      VARCHAR(50),
            PRIMARY KEY (ID),
            FOREIGN KEY (FK_Postleitzahl) REFERENCES Postleitgebiet(Postleitzahl)
              ON UPDATE CASCADE
              ON DELETE CASCADE
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Freizeitangebot (
            ID                   INT NOT NULL,
            FK_Postleitzahl      VARCHAR(10) NOT NULL,
            Art                  VARCHAR(50),
            PRIMARY KEY (ID),
            FOREIGN KEY (FK_Postleitzahl) REFERENCES Postleitgebiet(Postleitzahl)
              ON UPDATE CASCADE
              ON DELETE CASCADE
        );
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
