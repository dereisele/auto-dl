from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    CHANNEL = "sciencechannel"

    def setup(self, app):
        print("setup SC")
        self.parent = app
        self.parent.register_scraper('us_sciencechannelgo_com', self.scrape)
