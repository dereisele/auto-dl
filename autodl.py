"""Main file."""
from pluginbase import PluginBase
from dbmanager import DBManager
import configparser
import os

config = configparser.ConfigParser()


class AutoDl(object):
    """Main class."""

    scrappers = {}
    myDB = ""

    plugin_base = PluginBase(package='autodl.scrapper')

    def __init__(self):
        """Init main class."""
        global test
        self.load_config()
        self.init_config()
        self.myDB = DBManager(config["BASIC"]["DBLocation"])
        self.plugin_source = self.plugin_base.make_plugin_source(
                             searchpath=['./scrappers'])

        for plugin_name in self.plugin_source.list_plugins():
            plugin = self.plugin_source.load_plugin(plugin_name)
            plugin.Scrapper().setup(self)

        self.scrap()
        self.save_config()

    def init_config(self):
        """Setup config if nor exist."""
        basic_conf = {"DefaultLang": "de",
                      "DefaultLocation": "de",
                      "DBLocation": "./media.db"}

        network_conf = {"VPNStart": "windscribe connect {loc}",
                        "VPNStop": "windscribe disconnect"}

        if "BASIC" not in config.sections():
            config.add_section("BASIC")

        if "NETWORK" not in config.sections():
            config.add_section("NETWORK")

        for element in basic_conf:
            if element not in config["BASIC"]:
                config.set("BASIC", element, basic_conf[element])

        for element in network_conf:
            if element not in config["NETWORK"]:
                config.set("NETWORK", element, network_conf[element])

    def load_config(self):
        """Load config from config.ini."""
        if os.path.isfile('config.ini'):
            with open('config.ini', 'r') as configfile:
                config.read_file(configfile)

    def save_config(self):
        """Save config in config.ini."""
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def register_scrapper(self, name, scrapper):
        """Use to register a scrapper plugin."""
        self.scrappers[name] = scrapper

        if "SCRAPPER" not in config.sections():
            config.add_section("SCRAPPER")

        if name not in config["SCRAPPER"]:
            config["SCRAPPER"][name] = "True"

    def scrap(self):
        """Execute all scrappers."""
        for name, s in sorted(self.scrappers.items()):
            print('{}: {}'.format(name, s()))
            print('')


if __name__ == '__main__':
    AutoDl()
