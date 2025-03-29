import re
import os
import string
from urllib.request import urlopen
import mysql.connector
import html

def run():
    db=connect()
    cursor = db.cursor()
    scrape(db, cursor)

def scrape(db, cursor):
    url = "https://www.in-berlin-brandenburg.com/Berliner_Bezirke/plz-berlin.html"
    page = urlopen(url)
    html_bytes = page.read()
    htmlText = html_bytes.decode("utf-8")

    # Reguläre Ausdrücke für Bezirke, Ortsteile und PLZ
    bezirk_pattern = re.compile(r"<h3 id=.*>(?:Die Postleitzahlen von )?(.*?)<\/h3>")
    ortsteil_pattern = re.compile(r"<h4>(?:[PLZ, Postleitzahl] vom Ortsteil )?(.*?)<\/h4>")
    plz_pattern = re.compile(r"<li>(\d{5})<\/li>")

    bezirk = None
    ortsteil = None

    # HTML Zeilenweise durchsuchen
    for line in htmlText.split("\n"):
        bezirk_match = bezirk_pattern.search(line)
        ortsteil_match = ortsteil_pattern.search(line)
        plz_match = plz_pattern.findall(line)

        if bezirk_match:
            bezirk = html.unescape(bezirk_match.group(1).strip())
    
        elif ortsteil_match:
            ortsteil = html.unescape(ortsteil_match.group(1).strip())
            insert_data = (
                    ortsteil,
                    bezirk.replace("Die Postleitzahlen ", "").replace("Berlin ", "").replace(" Hohenschönhausen", "")
                )
            # SQL-Befehl mit Platzhaltern
            insert = """
                    INSERT IGNORE INTO Ortsteil (
                        Name, FK_Bezirksname
                    ) 
                VALUES (%s, %s)
            """
            cursor.execute(insert, insert_data)
    
        elif plz_match and ortsteil and bezirk:
            for plz in plz_match:
                insert_data = (
                    plz,
                    ortsteil,
                )
                # SQL-Befehl mit Platzhaltern
                insert = """
                        INSERT INTO Postleitgebiet (
                        Postleitzahl, FK_Ortsteil
                    ) 
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE
                        FK_Ortsteil = VALUES(FK_Ortsteil);
                """
                cursor.execute(insert, insert_data)

    db.commit()
    cursor.close()
    db.close()

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

run()