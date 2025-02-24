import re
import string
from urllib.request import urlopen


def run():
    supermarkets = []
    # Liste mit typischen Discountern (kann erweitert werden)
    discounter_keywords = [
    "Aldi", "Lidl", "Penny", "Netto", "Norma"
    ]
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
            # Adressen und Namen 'schön machen'
            name = name.replace("&nbsp;", "")
            adress = adress.replace("&ndash;\n", " ").replace("&nbsp;", " ").replace("\n      ", "").replace("        ", "")
            # discounter? ermitteln
            discounter = any(discounter in name for discounter in discounter_keywords)
            # PLZ mit Regex extrahieren (5-stellige Zahl am Anfang der Adresse)
            plz_match = re.search(r"\b\d{5}\b", adress)
            plz = plz_match.group(0) if plz_match else "Unbekannt"
            # Alle Daten in supermarkets gespeichert
            supermarkets.append({"plz": plz,"name": name, "adresse": adress, "discounter?": discounter})


    return supermarkets
    # Hier später einfügen in DB



print(run())