"""Tools for scrapers."""
import staticdata


class BasicScraper(object):
    """Class to inherite scrapers."""

    def __init__(self):
        self.SCRAPER_ID = self.SCRAPER_ID.split(".")[-1]

    def getOVLang(self, name):
        """Return original language of TV Show."""
        print("Get OV-Lang for " + name)
        return staticdata.OV_LANG.get(name, staticdata.OV_DEFAULT)

    def setup(self, app):
        """Setup scraper plugin."""
        print("Setup", self.SCRAPER_ID)
        self.parent = app
        self.parent.register_scraper(self.SCRAPER_ID, self.scrape)

    def addShow(self, name, lang):
        """Add show to DB and return showID."""
        self.parent.myDB.addShow(name, lang)
        myShowID = self.parent.myDB.getShowID(name, lang)
        return myShowID

    def addEpisode(self, showID, seasonNumber, episodeNumber, episodeTitle,
                   url, lang, quality):
        """Add episode to DB."""
        self.parent.myDB.addEpisode(showID, seasonNumber,
                                    episodeNumber, episodeTitle,
                                    url, "de", quality)

    def addConfigKey(self, key, default):
        """Allow scrapers to add config keys."""
        self.parent.addConfigKey(self.SCRAPER_ID, key, default)

    def getConfigKey(self, key):
        """Get config key."""
        return dict(self.parent.config)[self.SCRAPER_ID][key]
