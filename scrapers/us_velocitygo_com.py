from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    CHANNEL = "velocity"

    def setup(self, app):
        print("setup Velocity")
        self.parent = app
        self.parent.register_scraper('us_velocitygo_com', self.scrape)
