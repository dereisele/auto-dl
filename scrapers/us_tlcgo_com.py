from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    CHANNEL = "tlc"

    def setup(self, app):
        print("setup TLC")
        self.parent = app
        self.parent.register_scraper('us_tlcgo_com', self.scrape)
