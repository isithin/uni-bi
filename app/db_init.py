import mysql.connector
import time
import os

# Warte, bis MySQL verfügbar ist
time.sleep(10)

# Verbindung zu MySQL herstellen
def connect(user, password, database):
    try:
        db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=user,
            password=password,
            database=database
        )
        return db
    except Exception as e:
        print(e)
        return None

def create_databases(cursor):
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

def grant_privileges(cursor):

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

def create_table(cursor):

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
            Name                        VARCHAR(50) NOT NULL,
            Durchschnittsalter          DECIMAL(4,1), 
            Armutsgefährdungsquote      DECIMAL(4,1),
            Geringqualifikationsquote   DECIMAL(4,1),
            Erwerbslosigkeitsquote      DECIMAL(4,1),
            Straftaten_gesamt           INT,
            Raub                        INT,
            Strassenraub                INT,
            Koerperverletzung_gesamt    INT,
            Gefaehrliche_Koerperverletzung INT,
            Freiheitsberaubung          INT,
            Diebstahl_gesamt            INT,
            Diebstahl_Kraftwagen        INT,
            Diebstahl_Kfz               INT,
            Fahrraddiebstahl            INT,
            Wohnungseinbruch            INT,
            Branddelikte_gesamt         INT,
            Brandstiftung               INT,
            Sachbeschaedigung_gesamt    INT,
            Sachbeschaedigung_Graffiti  INT,
            Rauschgiftdelikte           INT,
            Kieztaten                   INT,
            PRIMARY KEY (Name)
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Postleitgebiet (
            Postleitzahl         VARCHAR(10) NOT NULL,
            Ortsteil             VARCHAR(50),
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
            Preis_kalt           DECIMAL(10,2),
            Groesse              INT,
            Anzahl_Räume         INT,
            Etage                INT,
            Baujahr              INT,
            Aufzug               BOOLEAN,
            Parkplaetze          BOOLEAN,
            Kueche               BOOLEAN,
            Balkon               BOOLEAN,
            Garten               BOOLEAN,
            Terrasse             BOOLEAN,
            Energie              VARCHAR(20),
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
            Name                 VARCHAR(50),
            Ortsteil             VARCHAR(10) NOT NULL,
            Preisklasse          INT,
            S_Bahn               BOOlEAN,
            Regionalverkehr      BOOLEAN,
            Fernverkehr          BOOLEAN,
            U_Bahn               BOOLEAN,
            PRIMARY KEY (ID),
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
    db = connect("root",os.getenv("MYSQL_ROOT_PASSWORD"),"mysql")
    if db is not None:
        print("Connected to MySQL")
    else:
        print("Connection to MySQL failed")
    cursor = db.cursor()
    create_databases(cursor)
    grant_privileges(cursor)
    cursor.close()
    db.close()

    db = connect(os.getenv("MYSQL_USER"),os.getenv("MYSQL_PASSWORD"),"bi")
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
