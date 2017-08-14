from scrapertemplates import us_discovery


class Scraper(us_discovery.DiscoveryScraper):

    SCRAPER_ID = __name__
    CHANNEL = "animalplanet"
