from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    CHANNEL = "destinationamerica"

    def setup(self, app):
        print("setup destinationamerica")
        self.parent = app
        self.parent.register_scraper('us_destinationamericago_com', self.scrape)
