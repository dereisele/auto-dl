from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    CHANNEL = "animalplanet"

    def setup(self, app):
        print("setup animalplanet")
        self.parent = app
        self.parent.register_scraper('us_animalplanetgo_com', self.scrape)
