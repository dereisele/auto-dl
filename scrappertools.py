"""Tools for scrappers."""
import staticdata


class BasicScrapper(object):
    """Class to inherite scrappers."""

    def getOVLang(self, name):
        """Return original language of TV Show."""
        print("Get OV-Lang for " + name)
        return staticdata.OV_LANG.get(name, staticdata.OV_DEFAULT)
