"""Handles download incl. VPN and naming."""
import youtube_dl
import os
import subprocess
import time


class Downloader(object):
    """Handles download incl. VPN and naming."""

    dl_config = dict()
    VPN = False

    def __init__(self, app):
        """Init class and load config as dict."""
        self.parent = app
        self.dl_config = dict(self.parent.config)

    def release(self, forced=False):
        """Disable VPN."""
        if self.VPN or forced:
            cmdline = self.dl_config["NETWORK"]["vpnstop"].split()
            proc = subprocess.Popen(cmdline)

    def setLocation(self, loc):
        """Activate VPN if neccessary."""
        myLoc = self.parent.config["BASIC"]["defaultlocation"]
        if loc not in (myLoc, "any", self.VPN):
            print(myLoc + " is not " + loc)
            cmdline = self.dl_config["NETWORK"]["vpnstart"].format(loc=loc).split()
            proc = subprocess.Popen(cmdline)
            self.VPN = loc
            time.sleep(15)

        if loc in (myLoc, "any"):
            self.release()

    def downloadQueue(self):
        """Fetch and download queue."""
        queue = self.parent.myDB.getDownloadQueue()
        for item in queue:
            self.download(item)

    def download(self, item):
        """Download item from queue."""
        dl_id, episode_id, season, episode, name, url, loc, _, state, show = item

        self.setLocation(loc)

        season = "%02d" % season
        episode = "%02d" % episode

        os.makedirs(self.dl_config["BASIC"]["medialocation"]
                    + "/" + show.replace(" ", "-"), exist_ok=True)
        os.chdir(self.dl_config["BASIC"]["medialocation"]
                 + "/" + show.replace(" ", "-"))

        self.parent.myDB.updateQueueState(episode_id, "1")

        ydl_opts = dict()
        ydl_opts["outtmpl"] = "{}_{}_S{}E{}.%(ext)s".format(show.replace(" ", "-"),
                                                            name.replace(" ", "-"),
                                                            season, episode)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        self.parent.myDB.removeEpisodeFromQueue(episode_id)
        self.parent.myDB.updateEpisodeDlState(episode_id, 1)

    def __del__(self):
        self.release(True)
