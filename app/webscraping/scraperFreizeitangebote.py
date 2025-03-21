import requests
import json
import mysql.connector
import os

def run():
    db=connect()
    cursor = db.cursor()
    scrape(db, cursor)

def scrape(db, cursor):
    # 🌍 Berlin (Mitte) als Mittelpunkt
    BERLIN_CENTER = "52.5200,13.4050"
    RADIUS = 20000  # 20 km

    # Overpass API Abfrage (z. B. Restaurants + Parks + Spielplätze)
    query = f"""
    [out:json];
    (
      node["amenity"="restaurant"](around:{RADIUS},{BERLIN_CENTER});
      node["leisure"="park"](around:{RADIUS},{BERLIN_CENTER});
      node["leisure"="playground"](around:{RADIUS},{BERLIN_CENTER});
    );
    out body;   
    """

    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": query})

    if response.status_code == 200:
        data = response.json()
        for element in data["elements"]:
            name = element.get("tags", {}).get("name", "Unbekannt")
            typ = element.get("tags", {}).get("amenity") or element.get("tags", {}).get("leisure")
            lat, lon = element["lat"], element["lon"]
            plz = get_postal_code(lat, lon)

            sql = """
                    INSERT INTO Freizeitangebot (FK_Postleitzahl, Name, Art) 
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE Name = VALUES(Name)
             """
            cursor.execute(sql, (plz, name, typ))
            db.commit()

    else:
        print("Fehler beim Abrufen der Daten.")

def get_postal_code(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url, headers={"User-Agent": "FreizeitScraper"})
    data = response.json()
    
    return data.get("address", {}).get("postcode", "Keine PLZ gefunden")

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