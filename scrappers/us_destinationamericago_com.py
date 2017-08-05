from scrappertemplates import us_discovery


class Scrapper(us_discovery.DiscoveryScrapper):

    CHANNEL = "destinationamerica"

    def setup(self, app):
        print("setup destinationamerica")
        self.parent = app
        self.parent.register_scrapper('us_destinationamericago_com', self.scrap)
