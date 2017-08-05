from scrappertemplates import us_discovery


class Scrapper(us_discovery.DiscoveryScrapper):

    CHANNEL = "tlc"

    def setup(self, app):
        print("setup TLC")
        self.parent = app
        self.parent.register_scrapper('us_tlcgo_com', self.scrap)
