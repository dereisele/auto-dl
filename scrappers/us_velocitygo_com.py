from scrappertemplates import us_discovery


class Scrapper(us_discovery.DiscoveryScrapper):

    CHANNEL = "velocity"

    def setup(self, app):
        print("setup Velocity")
        self.parent = app
        self.parent.register_scrapper('us_velocitygo_com', self.scrap)
