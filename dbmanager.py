class AutoDl(object):
    """Main class."""

    scrappers = {}

    plugin_base = PluginBase(package='auto-dl.scrapper')

    def __init__(self):
        """Init main class."""
        self.load_config()
        self.init_config()
        self.plugin_source = self.plugin_base.make_plugin_source(
                             searchpath=['./scrapper'])

        for plugin_name in self.plugin_source.list_plugins():
            plugin = self.plugin_source.load_plugin(plugin_name)
            plugin.setup(self)
        self.scrap()
        self.save_config()

    def init_config(self):
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


class DBManager(object):
    """Handle Database."""

    connection = ""
    cursor = ""

    def createTable(self):
        """Create Table for shows and episodes if not exists."""

        #Shows
        sql_command = """
        CREATE TABLE IF NOT EXISTS shows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lang VARCHAR(2),
        name VARCHAR(50));"""

        self.cursor.execute(sql_command)

        #Episodes
        sql_command = """
        CREATE TABLE IF NOT EXISTS episodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        show_id INTEGER,
        season INTEGER,
        episode INTEGER,
        name VARCHAR(50),
        url VARCHAR(50),
        loc VARCHAR(5),
        quality VARCHAR(12),
        download VARCHAR(1) DEFAULT '0');"""

        self.cursor.execute(sql_command)

        #Shows to Download
        sql_command = """
        CREATE TABLE IF NOT EXISTS shows_dl (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lang VARCHAR(2),
        name VARCHAR(50));"""

        self.cursor.execute(sql_command)

        #Episodes to Download
        sql_command = """
        CREATE TABLE IF NOT EXISTS episodes_dl(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            episode_id INTEGER,
            state VARCHAR(1) DEFAULT '0',
            UNIQUE(episode_id)
        );"""

        self.cursor.execute(sql_command)


    def addShow(self, name, lang=config["BASIC"]["defaultlang"]):
        """Add show to DB if not exists."""
        name = clear(name)
        print(name + ", " + lang)
        #sql_command = "INSERT INTO shows (name, lang) VALUES (?, ?)"
        sql_command = "INSERT INTO shows (name, lang) SELECT \"" + name + "\", \"" + lang + "\" WHERE NOT EXISTS(SELECT * FROM shows WHERE name = \"" + name + "\" AND lang = \"" + lang + "\")"

        self.cursor.execute(sql_command)

    def addEpisode(self, show_id, season, episode, name, url, loc="any", quality="unknown"):
        """Add episode to DB if not exists."""
        name = clear(name)
        #print(name + ", " + url)
        #sql_command = "INSERT INTO episodes (show_id, season, episode, name, url) VALUES (?, ?, ?, ?, ?)"
        sql_command = "INSERT INTO episodes (show_id, season, episode, name, url, loc, quality) SELECT \"" + str(show_id) + "\", \"" + str(season) + "\", \"" + str(episode) + "\", \"" + name + "\", \"" + url + "\", \"" + loc + "\", \"" + quality + "\" WHERE NOT EXISTS(SELECT * FROM episodes WHERE show_id = \"" + str(show_id) + "\" AND season = \"" + str(season) + "\" AND episode = \"" + str(episode) + "\")"


        #self.cursor.execute(sql_command, (int(show_id), int(season), int(episode), name, url))
        self.cursor.execute(sql_command)

    def getShowID(self, name):
        """Return show id."""
        name = clear(name)
        sql_command = "SELECT id FROM shows WHERE name = \"" + name + "\""
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()[0]

    def getShowIDs(self, name):
        """Return ALL show id. (For debugging)."""
        name = clear(name)
        sql_command = "SELECT id FROM shows WHERE name = \"" + name + "\""
        self.cursor.execute(sql_command)
        return self.cursor.fetchall()

    def matchEpisodes(self):
        """Add Episodes to download queue."""
        sql_command = """
        INSERT OR IGNORE INTO episodes_dl (episode_id)
        SELECT episodes.id FROM shows, episodes, shows_dl
        WHERE episodes.show_id = shows.id
        AND episodes.download = "0"
        AND shows.name = shows_dl.name
        """
        self.cursor.execute(sql_command)
        return self.cursor.fetchall()

    def getEpisodesToDL(self):
        """Get download infos of episodes to download."""
        sql_command = """
        SELECT episodes.*, shows.name FROM episodes, episodes_dl, shows
        WHERE shows.id = episodes.show_id
        AND episodes.id = episodes_dl.episode_id
        """
        self.cursor.execute(sql_command)
        return self.cursor.fetchall()

    def addShowToDL(self, name, lang):
        """Add show to DL queue."""
        sql_command = "INSERT INTO shows_dl (name, lang) VALUES (?, ?)"
        self.cursor.execute(sql_command, (name, lang))

    def updateDlState(self, episode_id, state):
        """Update DL State of item in DL queue."""
        sql_command = "UPDATE episodes_dl SET state = ? WHERE episode_id = ?"
        self.cursor.execute(sql_command, (state, episode_id))

    def removeEpisodeFromDL(self, episode_id):
        """Remove item from DL queue."""
        sql_command = "DELETE FROM episodes_dl WHERE episode_id = ?"
        self.cursor.execute(sql_command, (episode_id,))

    def updateEpisodeDlState(self, episode_id, state):
        """Update DL State of item in episodes list."""
        sql_command = "UPDATE episodes SET download = ? WHERE id = ?"
        self.cursor.execute(sql_command, (state, episode_id))

    def __init__(self):
        """Init and connect DB."""
        self.connection = sqlite3.connect("test.db")
        self.cursor = self.connection.cursor()
        self.createTable()

    def __del__(self):
        """Disconnect DB."""
        print("Disconected DB")
        self.connection.commit()
        self.connection.close()
