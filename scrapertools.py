"""Tools for scrapers."""
import staticdata


class BasicScraper(object):
    """Class to inherite scrapers."""

    def getOVLang(self, name):
        """Return original language of TV Show."""
        print("Get OV-Lang for " + name)
        return staticdata.OV_LANG.get(name, staticdata.OV_DEFAULT)
