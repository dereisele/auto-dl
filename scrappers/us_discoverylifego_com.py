from scrappertemplates import us_discovery


class Scrapper(us_discovery.DiscoveryScrapper):

    CHANNEL = "discoverylife"

    def setup(self, app):
        print("setup discoverylifego")
        self.parent = app
        self.parent.register_scrapper('us_discoverylifego_com', self.scrap)
