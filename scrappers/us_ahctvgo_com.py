from scrappertemplates import us_discovery


class Scrapper(us_discovery.DiscoveryScrapper):

    CHANNEL = "ahctv"

    def setup(self, app):
        print("setup AHCTV")
        self.parent = app
        self.parent.register_scrapper('us_ahctvgo_com', self.scrap)
