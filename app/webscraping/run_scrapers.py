import scraperImmowelt
import scraperBezirk
import scraperPostleitgebiet
import scraperWohnungsboerse
import scraperSupermarkt
import scraperHaltestellen

# Diese Datei ausführen, um die beiden Scraper zu starten
if __name__ == "__main__":

    # # Immowelt scraper starten
    # print("📡 Scraping Immowelt...")
    # scraperImmowelt.run()
    # print("")

    # Bezirk scraper starten
    print("📡 Scraping Bezirke...")
    scraperBezirk.run()
    print("")

    # Postleitgebiet scraper starten
    print("📡 Scraping Wohnungsboerse...")
    scraperPostleitgebiet.run()
    print("")

    # Supermarkt scraper starten
    print("📡 Scraping Supermärkte...")
    scraperSupermarkt.run()
    print("")

    # Wohnungsboerse scraper starten
    print("📡 Scraping Wohnungsboerse...")
    scraperWohnungsboerse.run()
    print("")

    # Freizeitangebote scraper starten
    print("📡 Scraping Freizeitangebote...")
    scraperFreizeitangebote.run()
    print("")

    # Haltestellen scraper starten
    print("📡 Scraping Haltestellen...")
    scraperHaltestellen.run()
    print("")


    # Ergebnisse anzeigen
    print("✅ All scrapers have finished.")
    print("💾 The data has been saved to DB")
