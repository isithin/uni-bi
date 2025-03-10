import re
import os
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

    # Daten speichern
    bezirk = None

    # HTML Zeilenweise durchsuchen
    for line in htmlText.split("\n"):
        bezirk_match = bezirk_pattern.search(line)

        if bezirk_match:
            bezirk = html.unescape(bezirk_match.group(1).strip())
            data = "'"+bezirk+"'"
            cursor.execute("INSERT IGNORE INTO Bezirk (Name) VALUES ("+data+")")
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