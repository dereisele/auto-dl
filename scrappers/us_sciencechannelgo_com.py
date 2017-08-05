from scrappertemplates import us_discovery


class Scrapper(us_discovery.DiscoveryScrapper):

    CHANNEL = "sciencechannel"

    def setup(self, app):
        print("setup SC")
        self.parent = app
        self.parent.register_scrapper('us_sciencechannelgo_com', self.scrap)
