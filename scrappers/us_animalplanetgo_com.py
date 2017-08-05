from scrappertemplates import us_discovery


class Scrapper(us_discovery.DiscoveryScrapper):

    CHANNEL = "animalplanet"

    def setup(self, app):
        print("setup animalplanet")
        self.parent = app
        self.parent.register_scrapper('us_animalplanetgo_com', self.scrap)
