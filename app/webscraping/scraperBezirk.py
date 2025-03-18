import pandas as pd
import os
from urllib.request import urlopen
import mysql.connector

def run():
    db=connect()
    cursor = db.cursor()
    scrape(db, cursor)

def scrape(db, cursor):
    berliner_bezirke = {
        "Mitte": [],
        "Friedrichshain-Kreuzberg": [],
        "Pankow": [],
        "Charlottenburg-Wilmersdorf": [],
        "Spandau": [],
        "Steglitz-Zehlendorf": [],
        "Tempelhof-Schöneberg": [],
        "Neukölln": [],
        "Treptow-Köpenick": [],
        "Marzahn-Hellersdorf": [],
        "Lichtenberg": [],
        "Reinickendorf": []
    }

    # Excel-Datei einlesen
    file_path_durchschnittsalter = r"https://download.statistik-berlin-brandenburg.de/8b004f55d4a74860/f1f0744a299e/SB_A01-05-00_2024h01_BE.xlsx"
    file_path_finanzen = r"https://download.statistik-berlin-brandenburg.de/e46d505407f9f2ab/665ce591962b/AfS_Tabellen_Sozialbericht_2022_BBB.xlsx"
    file_path_kriminalität = r"https://www.kriminalitaetsatlas.berlin.de/K-Atlas/bezirke/Fallzahlen%26HZ%202014-2023.xlsx"

    df_durchschnittsalter = pd.read_excel(file_path_durchschnittsalter, sheet_name="T3 T4", skiprows=45, usecols="C:N", engine="openpyxl")
    df_armutsgef = pd.read_excel(file_path_finanzen, sheet_name="A1a I Armutsgef regional", usecols="B:T", engine="openpyxl")
    df_geringqualifizierte = pd.read_excel(file_path_finanzen, sheet_name="D1 Geringqualifizierte regional", usecols="B:T", engine="openpyxl")
    df_erwerbslosigkeit = pd.read_excel(file_path_finanzen, sheet_name="E4 Erwerbsl. Haushalte regional", usecols="B:T", engine="openpyxl")
    df_kriminalität = pd.read_excel(file_path_kriminalität, sheet_name="Fallzahlen_2023", skiprows=4)

    # Durchschnittsalter der Einwohnerinnen und Einwohner in Berlin 2024:
    for column in df_durchschnittsalter.columns:
        for bezirk in berliner_bezirke:
            if bezirk[:3] == column[:3]:  # Die ersten 3 Buchstaben des Bezirk-Namens mit der Spalten-Überschrift vergleichen
                # Das Durchschnittsalter ist in der letzten Zeile der jeweiligen Spalte
                durchschnittsalter = df_durchschnittsalter[column].iloc[-1]  # Letzte Zeile dieser Spalte
                # Das Dictionary aktualisieren, indem das Durchschnittsalter zu dem Bezirk hinzugefügt wird
                berliner_bezirke[bezirk].append(durchschnittsalter)

    # A1a I Armutsgefährdungsquoten der Bevölkerung 2022:
    for bezirk, armutsGefQuote in zip(df_armutsgef["Unnamed: 1"].iloc[7:19], df_armutsgef["Unnamed: 19"].iloc[7:19]):
        berliner_bezirke[bezirk].append(armutsGefQuote)

    # D1 Anteil der ab 25-Jährigen mit niedrigem Bildungsstand (ISCED 0-2)¹ an der gleichaltrigen Bevölkerungsgruppe 2022:
    for bezirk, anteilGeringq in zip(df_geringqualifizierte["Unnamed: 1"].iloc[6:18], df_geringqualifizierte["Unnamed: 19"].iloc[6:18]):
        berliner_bezirke[bezirk].append(anteilGeringq)

    # E4 Anteil der in Haushalten ohne Erwerbstätige lebenden unter 60-Jährigen 2022:
    for bezirk, erwerbslosigkeit in zip(df_erwerbslosigkeit["Unnamed: 1"].iloc[6:18], df_erwerbslosigkeit["Unnamed: 19"].iloc[6:18]):
        berliner_bezirke[bezirk].append(erwerbslosigkeit)

    # Häufigkeitszahlen (HZ) der Bezirke; Kriminalitätsatlas (PKS 2023)
    df_kriminalität.columns = [
        "LOR_Schluessel", "Bezirk", "Straftaten_gesamt", "Raub", "Strassenraub",
        "Koerperverletzung_gesamt", "Gefaehrliche_Koerperverletzung", 
        "Freiheitsberaubung", "Diebstahl_gesamt", "Diebstahl_Kraftwagen", 
        "Diebstahl_Kfz", "Fahrraddiebstahl", "Wohnungseinbruch", 
        "Branddelikte_gesamt", "Brandstiftung", "Sachbeschaedigung_gesamt", 
        "Sachbeschaedigung_Graffiti", "Rauschgiftdelikte", "Kieztaten"
    ]
    df_kriminalität.dropna(subset=["Bezirk"], inplace=True)
    df_kriminalität.head()

    for _, row in df_kriminalität.iterrows():
        bezirk_name = row["Bezirk"].strip()
        if bezirk_name in berliner_bezirke:
            berliner_bezirke[bezirk_name].extend([
                row["Straftaten_gesamt"], row["Raub"], row["Strassenraub"],
                row["Koerperverletzung_gesamt"], row["Gefaehrliche_Koerperverletzung"],
                row["Freiheitsberaubung"], row["Diebstahl_gesamt"], 
                row["Diebstahl_Kraftwagen"], row["Diebstahl_Kfz"], row["Fahrraddiebstahl"], 
                row["Wohnungseinbruch"], row["Branddelikte_gesamt"], row["Brandstiftung"], 
                row["Sachbeschaedigung_gesamt"], row["Sachbeschaedigung_Graffiti"], 
                row["Rauschgiftdelikte"], row["Kieztaten"]
            ])



    # Eintrag in Datenbank
    # SQL-Befehl mit Platzhaltern
    insert = """
    INSERT IGNORE INTO Kriminalitaet (
        Bezirk, Durchschnittsalter, Armutsgefährdungsquote, Geringqualifikationsquote,
        Erwerbslosigkeitsquote, Straftaten_gesamt, Raub, Strassenraub,
        Koerperverletzung_gesamt, Gefaehrliche_Koerperverletzung, Freiheitsberaubung,
        Diebstahl_gesamt, Diebstahl_Kraftwagen, Diebstahl_Kfz, Fahrraddiebstahl,
        Wohnungseinbruch, Branddelikte_gesamt, Brandstiftung,
        Sachbeschaedigung_gesamt, Sachbeschaedigung_Graffiti,
        Rauschgiftdelikte, Kieztaten
    ) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Daten aus dem Dictionary in die Tabelle einfügen
    for bezirk, daten_liste in berliner_bezirke.items():
        cursor.execute(insert, [bezirk] + daten_liste)

    # Änderungen in der Datenbank speichern
    db.commit()

    # Verbindung schließen
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