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
            user="root",
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            database="mysql"
        )
        return db
    except Exception as e:
        print(e)
        return None

def create_table(cursor):
    cursor.execute(
        """
        CREATE DATABASE IF NOT EXISTS grafana
        """
    )
    cursor.execute(
        """
        CREATE DATABASE IF NOT EXISTS bi
        """
    )

    # User anlegen
    grafana_user = "CREATE USER IF NOT EXISTS 'grafanaReader' IDENTIFIED BY '%s';" % os.getenv("GF_DATABASE_PASSWORD")
    bi_user = "CREATE USER IF NOT EXISTS 'bi' IDENTIFIED BY '%s';" % os.getenv("MYSQL_PASSWORD")
    
    cursor.execute(grafana_user)
    cursor.execute(bi_user)
    
    # Rechte vergeben
    cursor.execute(
        """
        GRANT SELECT ON bi.* TO 'grafanaReader'
        """
        )
    cursor.execute(
        """
        GRANT ALL PRIVILEGES ON grafana.* TO 'grafanaReader'
        """
        )
    # Test
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS example (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        )
        """
    )
    # Real Tables
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
            ID                   INT NOT NULL AUTO_INCREMENT,
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
            ID                   INT NOT NULL AUTO_INCREMENT,
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
            ID                   INT NOT NULL AUTO_INCREMENT,
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
            ID                   INT NOT NULL AUTO_INCREMENT,
            FK_Postleitzahl      VARCHAR(10) NOT NULL,
            Art                  VARCHAR(50),
            PRIMARY KEY (ID),
            FOREIGN KEY (FK_Postleitzahl) REFERENCES Postleitgebiet(Postleitzahl)
              ON UPDATE CASCADE
              ON DELETE CASCADE
        );
        """
    )

 
def insert_data(cursor, db, command):
    cursor.execute(command)
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
    insert_data(cursor, db, "INSERT INTO example (name) VALUES ('MiiiTest')")
    read_data(cursor) # Just for debugging

    cursor.close()
    db.close()

main()
