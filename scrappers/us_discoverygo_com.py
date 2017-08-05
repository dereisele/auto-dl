from scrappertemplates import us_discovery


class Scrapper(us_discovery.DiscoveryScrapper):

    CHANNEL = "discovery"

    def setup(self, app):
        print("setup Discovery")
        self.parent = app
        self.parent.register_scrapper('us_discoverygo_com', self.scrap)
