import scraperImmowelt
import scraperWohnungsboerse
import scraperSupermarkt

# Diese Datei ausführen, um die beiden Scraper zu starten
if __name__ == "__main__":

    # # Immowelt scraper starten
    # print("📡 Scraping Immowelt...")
    # scraperImmowelt.run()
    # print("")

    # Wohnungsboerse scraper starten
    print("📡 Scraping Wohnungsboerse...")
    scraperWohnungsboerse.run()
    print("")

    # Supermarkt scraper starten
    print("📡 Scraping Wohnungsboerse...")
    scraperSupermarkt.run()
    print("")


    # Ergebnisse anzeigen
    print("✅ All scrapers have finished.")
    print("💾 The data has been saved to the data folder.")
