import re
import string
from urllib.request import urlopen


def run():
    supermarkets = []
    BASE_URL = "https://berlin.kauperts.de/Adressen/Supermarkt/{letter}"
    # Durch alle Buchstaben A-Z iterieren
    for letter in string.ascii_uppercase:  # ['A', 'B', ..., 'Z']
        url = BASE_URL.format(letter=letter)
        print(f"Rufe Daten von {url} ab...")
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
<<<<<<< HEAD
            # Adressen und Namen 'schön machen'
            name = name.replace("&nbsp;", "")
=======
            # Adressen 'schön machen'
>>>>>>> c32701f (add scraper for supermarkets; add scraper to index.py)
            adress = adress.replace("&ndash;\n", " ").replace("&nbsp;", " ").replace("\n      ", "").replace("        ", "")
            # PLZ mit Regex extrahieren (5-stellige Zahl am Anfang der Adresse)
            plz_match = re.search(r"\b\d{5}\b", adress)
            plz = plz_match.group(0) if plz_match else "Unbekannt"
            # Alle Daten in supermarkets gespeichert
<<<<<<< HEAD
            supermarkets.append({"plz": plz,"name": name, "adresse": adress})
=======
            supermarkets.append({"plz": plz,"name": name.replace("&nbsp;", ""), "adresse": adress})
>>>>>>> c32701f (add scraper for supermarkets; add scraper to index.py)


    return supermarkets
    # Hier später einfügen in DB



print(run())