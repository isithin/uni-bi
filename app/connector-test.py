import mysql.connector
import time
import os

# Warte, bis MySQL verfügbar ist
time.sleep(10)

# Verbindung zu MySQL herstellen
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = db.cursor()

# Beispiel: Tabelle erstellen & Daten einfügen
cursor.execute("CREATE TABLE IF NOT EXISTS example (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
cursor.execute("INSERT INTO example (name) VALUES ('MiiiTest')")
db.commit()

# Daten abrufen
cursor.execute("SELECT * FROM example")
for row in cursor.fetchall():
    print(row)

cursor.close()
db.close()
