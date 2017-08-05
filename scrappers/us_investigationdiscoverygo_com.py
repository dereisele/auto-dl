from scrappertemplates import us_discovery


class Scrapper(us_discovery.DiscoveryScrapper):

    CHANNEL = "investigationdiscovery"

    def setup(self, app):
        print("setup IDS")
        self.parent = app
        self.parent.register_scrapper('us_investigationdiscoverygo_com', self.scrap)
