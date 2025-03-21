import re
import os
from urllib.request import urlopen
import mysql.connector
import html

def run():
    db=connect()
    cursor = db.cursor()
    scrape_Bahnhöfe_Haltepunkte(db, cursor)
    scrape_UBahnhöfe(db, cursor)

def scrape_Bahnhöfe_Haltepunkte(db, cursor):
    url = "https://de.wikipedia.org/wiki/Liste_der_Bahnh%C3%B6fe_und_Haltepunkte_in_Berlin"
    page = urlopen(url)
    html_bytes = page.read()
    htmlText = html_bytes.decode("utf-8")

    # Reguläre Ausdrücke für Name, Ortsteil, Preisklasse und Typ (später unterteilt in booleans)
    name_pattern = re.compile(r"<td><a href=\"\/wiki\/Bahnhof.*\">(.*)<\/a>")
    bertriebsart_pattern = re.compile(r"<td>([B,H][f,p])<\/td>")
    ortsteil_pattern = re.compile(r"<td><a href=\"\/wiki\/(?!Bahnstrecke).*\">(.*)<\/a><\/td>")
    preisklasse_pattern = re.compile(r"<td>(\d)<\/td>")
    typ_pattern = re.compile(r"<td>((?:[S, R, F]){1,5})")
    # Break-Pattern, um am Ende der Tabelle mit Scrapen aufzuhören
    break_pattern = re.compile(r"<p><b>Anmerkungen:</b>")

    name = None
    betriebsart = None
    ortsteil = None
    preisklasse = None
    typ = None

    # HTML Zeilenweise durchsuchen
    for line in htmlText.split("\n"):
        if break_pattern.search(line):
            break
        name_match = name_pattern.search(line)
        betriebsart_match = bertriebsart_pattern.search(line)
        ortsteil_match = ortsteil_pattern.search(line)
        preisklasse_match = preisklasse_pattern.search(line)
        typ_match = typ_pattern.search(line)

        if name_match:
            name = html.unescape(name_match.group(1).strip())

        elif betriebsart_match:
            betriebsart = betriebsart_match.group(1).strip()
            if betriebsart == "Bf": name = "Bahnhof " + name
            if betriebsart == "Hp": name = "Haltepunkt " + name
    
        elif ortsteil_match:
            ortsteil = html.unescape(ortsteil_match.group(1).strip())

        elif preisklasse_match:
            preisklasse = html.unescape(preisklasse_match.group(1).strip())

        elif typ_match and ortsteil and name and preisklasse:
            typ = html.unescape(typ_match.group(1).strip())

            insert_data = [name, ortsteil, preisklasse, 'S' in typ, 'R' in typ, 'F' in typ, False]

            insert = """
                    INSERT IGNORE INTO Haltestelle (
                        Name, FK_Ortsteil, Preisklasse, S_Bahn,
                        Regionalverkehr, Fernverkehr, U_Bahn
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert, insert_data)
            db.commit()

def scrape_UBahnhöfe(db, cursor):
    url = "https://de.wikipedia.org/wiki/Liste_der_Berliner_U-Bahnh%C3%B6fe"
    page = urlopen(url)
    html_bytes = page.read()
    htmlText = html_bytes.decode("utf-8")

    # Reguläre Ausdrücke für Name, Ortsteil, Preisklasse und Typ (später unterteilt in booleans)
    name_pattern = re.compile(r"<a href=\"\/wiki\/(?:U-)?Bahnhof.*\">(.*)<\/a>")
    linie_pattern = re.compile(r"<td style=\"text-align:center\" data-sort-value=\"(.*)\"><span")
    ortsteil_pattern = re.compile(r"<a href=\"\/wiki\/.*\">(.*)<\/a><\/td>")
    # Ignore-Pattern, um stillgelegte U-Bahnhöfe zu ignorieren
    ignore_pattern = re.compile(r"<tr class=\"hintergrundfarbe7\">")

    name = None
    ortsteil = None
    ignore = False


    # HTML Zeilenweise durchsuchen
    for line in htmlText.split("\n"):
        if ignore_pattern.search(line):
            ignore = True
        name_match = name_pattern.search(line)
        linie_match = linie_pattern.search(line)
        ortsteil_match = ortsteil_pattern.search(line)

        if name_match:
            name = "U-Bahnhof " + html.unescape(name_match.group(1).strip()).replace("Bahnhof ", "")


        elif linie_match and name:
            linie = html.unescape(linie_match.group(1).strip())
            name = name + " (" + linie + ")"


        elif ortsteil_match and name:
            ortsteil = html.unescape(ortsteil_match.group(1).strip())
            if ignore:
                ignore = False
                name = None
            else:
                insert_data = [name, ortsteil, False, False, False, True]

                insert = """
                        INSERT IGNORE INTO Haltestelle (
                            Name, FK_Ortsteil, S_Bahn,
                            Regionalverkehr, Fernverkehr, U_Bahn
                        )
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert, insert_data)
                db.commit()
                name = None


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
