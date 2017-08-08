"""Contains Database Manager."""
import sqlite3


class DBManager(object):
    """Handle Database."""

    connection = ""
    cursor = ""

    def prepareStr(self, string):
        """Escape unsave characters."""
        return string.replace("'", "\'").replace("\"", "")

    def createTable(self):
        """Create Table for shows and episodes if not exists."""
        # Shows
        sql_command = """
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lang VARCHAR(2),
            name VARCHAR(50),
            CONSTRAINT uShow UNIQUE(lang, name)
        )"""

        self.cursor.execute(sql_command)

        # Episodes
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
            download VARCHAR(1) DEFAULT '0',
            UNIQUE (show_id, season, episode)
        );"""

        self.cursor.execute(sql_command)

        # Shows to Download
        sql_command = """
        CREATE TABLE IF NOT EXISTS shows_dl (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lang VARCHAR(2),
            name VARCHAR(50)
        );"""

        self.cursor.execute(sql_command)

        # Episodes to Download
        sql_command = """
        CREATE TABLE IF NOT EXISTS episodes_dl(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            episode_id INTEGER,
            state VARCHAR(1) DEFAULT '0',
            UNIQUE(episode_id)
        );"""

        self.cursor.execute(sql_command)

    def addShow(self, name, lang):
        """Add show to DB if not exists."""
        name = self.prepareStr(name)
        print(name + ", " + lang)
        sql_command = """
        INSERT OR IGNORE INTO shows (name, lang)
            VALUES (?, ?)
        """

        self.cursor.execute(sql_command, (name, lang))

    def addEpisode(self, show_id, season, episode, name, url, loc="any", quality="unknown"):
        """Add episode to DB if not exists."""
        name = self.prepareStr(name)
        #sql_command = "INSERT INTO episodes (show_id, season, episode, name, url) VALUES (?, ?, ?, ?, ?)"
        #sql_command = ""
        #INSERT INTO episodes (show_id, season, episode, name, url, loc, quality)
        #SELECT \"" + str(show_id) + "\", \"" + str(season) + "\", \"" + str(episode) + "\", \"" + name + "\", \"" + url + "\", \"" + loc + "\", \"" + quality + "\" WHERE NOT EXISTS(SELECT * FROM episodes WHERE show_id = \"" + str(show_id) + "\" AND season = \"" + str(season) + "\" AND episode = \"" + str(episode) + "\")"

        sql_command = """
        INSERT OR IGNORE INTO episodes
            (show_id, season, episode, name, url, loc, quality)
                VALUES (?, ?, ?, ?, ?, ? ,?)
        """
        self.cursor.execute(sql_command, (int(show_id),
                                          int(season),
                                          int(episode),
                                          name,
                                          url,
                                          loc,
                                          quality))
        #self.cursor.execute(sql_command) """

    def getShowID(self, name, lang):
        """Return show id."""
        sql_command = """
        SELECT id FROM shows
            WHERE name = ?
            AND lang = ?"""

        self.cursor.execute(sql_command, (name, lang))
        return self.cursor.fetchone()[0]

    def getShowIDs(self, name):
        """Return ALL show id. (For debugging)."""
        sql_command = """
        SELECT id FROM shows
            WHERE name == ?
        """
        self.cursor.execute(sql_command, (name,))
        return self.cursor.fetchall()

    def matchEpisodes(self):
        """Add Episodes to download queue."""
        sql_command = """
        INSERT OR IGNORE INTO episodes_dl (episode_id)
            SELECT episodes.id FROM shows, episodes, shows_dl
                WHERE shows.name == shows_dl.name
                AND shows.lang == shows_dl.lang
                AND episodes.download == 0
                AND episodes.show_id == shows.id
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

    def updateQueueState(self, episode_id, state):
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

    def __init__(self, DBLocation):
        """Init and connect DB."""
        DBLocation = DBLocation
        self.connection = sqlite3.connect(DBLocation)
        self.cursor = self.connection.cursor()
        self.createTable()

    def __del__(self):
        """Disconnect DB."""
        print("Disconected DB")
        self.connection.commit()
        self.connection.close()
