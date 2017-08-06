from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    CHANNEL = "discovery"

    def setup(self, app):
        print("setup Discovery")
        self.parent = app
        self.parent.register_scraper('us_discoverygo_com', self.scrape)
