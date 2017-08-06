"""Main file."""
from pluginbase import PluginBase
from dbmanager import DBManager
from downloader import Downloader
import configparser
import os
import sys


class AutoDl(object):
    """Main class."""

    scrapers = {}
    myDB = ""
    config = configparser.ConfigParser()

    plugin_base = PluginBase(package='autodl.scraper')

    def __init__(self):
        """Init main class."""
        doScrape = True

        self.load_config()
        self.init_config()
        self.myDB = DBManager(self.config["BASIC"]["DBLocation"])
        self.plugin_source = self.plugin_base.make_plugin_source(
                             searchpath=['./scrapers'])

        for plugin_name in self.plugin_source.list_plugins():
            plugin = self.plugin_source.load_plugin(plugin_name)
            plugin.Scraper().setup(self)

        doScrape = "-noscrape" not in sys.argv
        doDl = "-nodl" not in sys.argv

        if "-add" in sys.argv:
            i = sys.argv.index("-add")
            newShow = sys.argv[i + 1]
            newLang = sys.argv[i + 2]
            self.myDB.addShowToDL(newShow, newLang)

        if doScrape:
            self.scrape()

        self.save_config()
        self.myDB.matchEpisodes()

        if doDl:
            self.myDL = Downloader(self)
            self.myDL.downloadQueue()

    def init_config(self):
        """Setup config if nor exist."""
        basic_conf = {"DefaultLang": "de",
                      "DefaultLocation": "de",
                      "DBLocation": "./media.db",
                      "MediaLocation": "./media"}

        network_conf = {"VPNStart": "windscribe connect {loc}",
                        "VPNStop": "windscribe disconnect"}

        if "BASIC" not in self.config.sections():
            self.config.add_section("BASIC")

        if "NETWORK" not in self.config.sections():
            self.config.add_section("NETWORK")

        for element in basic_conf:
            if element not in self.config["BASIC"]:
                self.config.set("BASIC", element, basic_conf[element])

        for element in network_conf:
            if element not in self.config["NETWORK"]:
                self.config.set("NETWORK", element, network_conf[element])

    def load_config(self):
        """Load config from config.ini."""
        if os.path.isfile('config.ini'):
            with open('config.ini', 'r') as configfile:
                self.config.read_file(configfile)

    def save_config(self):
        """Save config in config.ini."""
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def register_scraper(self, name, scraper):
        """Use to register a scraper plugin."""
        self.scrapers[name] = scraper

        if "SCRAPER" not in self.config.sections():
            self.config.add_section("SCRAPER")

        if name not in self.config["SCRAPER"]:
            self.config["SCRAPER"][name] = "True"

    def scrape(self):
        """Execute all scrapers."""
        for name, s in sorted(self.scrapers.items()):
            if self.config["SCRAPER"][name] == "True":
                print('{}: {}'.format(name, s()))
                print('')


if __name__ == '__main__':
    AutoDl()
