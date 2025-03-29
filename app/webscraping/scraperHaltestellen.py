import re
import os
from urllib.request import urlopen
import mysql.connector
import requests

def run():
    db=connect()
    cursor = db.cursor()
    scrape_API(db, cursor)

# Overpass API-Abfragefunktion
def fetch_osm_data(query):
    url = "http://overpass-api.de/api/interpreter"
    payload = f"[out:json][timeout:25];{query}" 
    response = requests.get(url, params={"data": payload})
    response.raise_for_status()  # Fehler ausgeben, falls HTTP-Fehler auftreten
    return response.json()

# Hauptfunktion zum Scrapen
def scrape_API(db, cursor):

    # Berlin als Suchbereich mit korrekter Syntax
    berlin_area_query = """
        area["name"="Berlin"]->.searchArea;
    """

    # Korrekte Overpass-Abfragen für Bahnhöfe
    queries = {
        "U-Bahn": f"""
            {berlin_area_query}
            node(area.searchArea)["railway"="subway_entrance"];
            out body;
        """,
        "S-Bahn": f"""
            {berlin_area_query}
            node(area.searchArea)["railway"="station"]["station"="light_rail"];
            out body;
        """,
        "Regional- und Fernverkehr": f"""
            {berlin_area_query}
            node(area.searchArea)["railway"="station"]["station"="train"];
            out body;
        """,
    }

    # Dictionary zum Speichern der Daten
    haltestellen = {}

    for typ, query in queries.items():
        print(f"🔎 Hole {typ}-Daten von OSM...")
        data = fetch_osm_data(query)
        # time.sleep(API_DELAY)  # Warten, um API-Limit nicht zu überschreiten

        for element in data.get("elements", []):
            name = element["tags"].get("name")
            plz = element.get("tags", {}).get("addr:postcode") or get_postal_code(element["lat"], element["lon"])

            # Initialisiere Haltestelle, falls noch nicht in der Liste
            if name not in haltestellen:
                haltestellen[name] = {"PLZ": plz, "S_Bahn": 0, "Regionalverkehr": 0, "Fernverkehr": 0, "U_Bahn": 0}

            # Setze die richtigen Flags
            if typ == "U-Bahn":
                haltestellen[name]["U_Bahn"] = 1
            elif typ == "S-Bahn":
                haltestellen[name]["S_Bahn"] = 1
            elif typ == "Regional- und Fernverkehr":
                haltestellen[name]["Regionalverkehr"] = 1
                haltestellen[name]["Fernverkehr"] = 1

    # SQL-Insert-Statement
    insert_sql = """
        INSERT INTO Haltestelle (Name, FK_Postleitzahl, S_Bahn, Regionalverkehr, Fernverkehr, U_Bahn)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            S_Bahn = VALUES(S_Bahn), 
            Regionalverkehr = VALUES(Regionalverkehr), 
            Fernverkehr = VALUES(Fernverkehr), 
            U_Bahn = VALUES(U_Bahn);
    """
    # Daten in die MySQL-Tabelle einfügen
    for name, data in haltestellen.items():
        cursor.execute(insert_sql, (name, data["PLZ"], data["S_Bahn"], data["Regionalverkehr"], data["Fernverkehr"], data["U_Bahn"]))

    db.commit()
    cursor.close()
    db.close()
    print("✅ Alle Haltestellen wurden erfolgreich gespeichert!")

def get_postal_code(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url, headers={"User-Agent": "FreizeitScraper"})
    data = response.json()
    address = data.get("address", {})
    if "Berlin" in address.get("city", "") or "Berlin" in address.get("state", ""):
        return address.get("postcode", "Keine PLZ")


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
