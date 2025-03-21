import os
import re
import string

import mysql.connector
from urllib.request import urlopen

def run():
    db=connect()
    cursor = db.cursor()
    scrape(db, cursor)

def scrape(db, cursor):
    # Liste mit typischen Discountern (kann erweitert werden)
    discounter_keywords = [
    "aldi", "lidl", "penny", "netto", "norma"
    ]
    BASE_URL = "https://berlin.kauperts.de/Adressen/Supermarkt/{letter}"
    # Durch alle Buchstaben A-Z iterieren
    for letter in string.ascii_uppercase:  # ['A', 'B', ..., 'Z']
        url = BASE_URL.format(letter=letter)
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        # Filtern aller Markt-Namen auf der Seite
        marketNamePattern = r"<td class=\"updated\"><a href=\".*\">(.*)<\/a><\/td>"
        marketNames = re.findall(marketNamePattern, html)
        # Filtern aller Adressen auf der Seite
        locationPattern = r"<td class=\"secondary zip-city\">\n(.*\n.*\n.*)<\/td>"
        locations = re.findall(locationPattern, html)
        for name, adress in zip(marketNames, locations):
            # Adressen und Namen 'schön machen'
            name = "'"+name.replace("&nbsp;", "").replace("&amp;", "&")+"'"
            adress = adress.replace("&ndash;\n", " ").replace("&nbsp;", " ").replace("\n      ", "").replace("        ", "")
            # PLZ mit Regex extrahieren (5-stellige Zahl am Anfang der Adresse)
            plz_match = re.search(r"\b\d{5}\b", adress)
            plz = plz_match.group(0) if plz_match else "'Unbekannt'"
            # Ermitteln, ob Discounter
            discounter = 0
            if(any(discounter in name.lower() for discounter in discounter_keywords)): discounter = 1
            # Alle Daten in Datenbank gespeichert
            data = plz + ", " + name + ", " + str(discounter)
            cursor.execute("INSERT IGNORE INTO Supermarkt (FK_Postleitzahl, Name, Discounter) VALUES ("+data+")")
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

