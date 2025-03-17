import pandas as pd
import requests
from io import BytesIO
from sqlalchemy import create_engine
import os

def run():
    # MySQL-Datenbankverbindung
    DB_USER = os.getenv("MYSQL_USER")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
    DB_HOST = os.getenv("MYSQL_HOST")
    DB_NAME = os.getenv("MYSQL_DATABASE")

    # Verbindung zur Datenbank herstellen
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

    # URL der Excel-Datei
    url = "https://www.kriminalitaetsatlas.berlin.de/K-Atlas/bezirke/Fallzahlen%26HZ%202014-2023.xlsx"

    # Datei herunterladen
    response = requests.get(url)
    xls = pd.ExcelFile(BytesIO(response.content))

    # Relevantes Sheet laden (2023er Daten)
    df = pd.read_excel(xls, sheet_name="Fallzahlen_2023", skiprows=4)

    # Erste beiden Spalten umbenennen (falls nötig)
    df.rename(columns={df.columns[0]: "LOR_Schluessel", df.columns[1]: "Bezirk"}, inplace=True)

    # Leere Zeilen entfernen
    df.dropna(subset=["LOR_Schluessel", "Bezirk"], inplace=True)

    # Daten in MySQL-Tabelle schreiben
    df.to_sql("kriminalitaet", con=engine, if_exists="replace", index=False)

    print("✅ Daten erfolgreich in Bi-DB importiert!")