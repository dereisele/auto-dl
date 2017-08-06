from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    CHANNEL = "investigationdiscovery"

    def setup(self, app):
        print("setup IDS")
        self.parent = app
        self.parent.register_scraper('us_investigationdiscoverygo_com', self.scrape)
