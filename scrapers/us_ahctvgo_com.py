from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    CHANNEL = "ahctv"

    def setup(self, app):
        print("setup AHCTV")
        self.parent = app
        self.parent.register_scraper('us_ahctvgo_com', self.scrape)
