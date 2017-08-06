from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    CHANNEL = "discoverylife"

    def setup(self, app):
        print("setup discoverylifego")
        self.parent = app
        self.parent.register_scraper('us_discoverylifego_com', self.scrape)
