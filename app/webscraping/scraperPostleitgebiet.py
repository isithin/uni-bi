import re
import string
from urllib.request import urlopen
import html


def run():
    url = "https://www.in-berlin-brandenburg.com/Berliner_Bezirke/plz-berlin.html"
    page = urlopen(url)
    html_bytes = page.read()
    htmlText = html_bytes.decode("utf-8")

    # Reguläre Ausdrücke für Bezirke, Ortsteile und PLZ
    bezirk_pattern = re.compile(r"<h3 id=.*>(?:Die Postleitzahlen von )?(.*?)<\/h3>")
    ortsteil_pattern = re.compile(r"<h4>(?:PLZ vom Ortsteil )?(.*?)<\/h4>")
    plz_pattern = re.compile(r"<li>(\d{5})<\/li>")

    # Daten speichern
    plz_data = []
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
    
        elif plz_match and ortsteil and bezirk:
            for plz in plz_match:
                plz_data.append({"PLZ": plz, "Ortsteil": ortsteil, "Bezirk": bezirk})
    


    return plz_data
    # Hier später einfügen in DB

    

print(run())