import youtube_dl
import os
import subprocess
import time


class Downloader(object):
    dl_config = dict()

    def __init__(self, app):
        self.parent = app
        self.dl_config = dict(self.parent.config)

    def downloadQueue(self):
        queue = self.parent.myDB.getEpisodesToDL()
        for item in queue:
            self.download(item)

    def download(self, item):
        dl_id, episode_id, season, episode, name, url, loc, _, state, show = item

        if not loc == self.dl_config["BASIC"]["defaultlocation"]:
            cmdline = self.dl_config["NETWORK"]["vpnstart"].format(loc=loc).split()
            proc = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
            time.sleep(2)

        season = "%02d" % season
        episode = "%02d" % episode

        os.makedirs(self.dl_config["BASIC"]["medialocation"]
                    + "/" + show.replace(" ", "-"), exist_ok=True)
        os.chdir(self.dl_config["BASIC"]["medialocation"]
                 + "/" + show.replace(" ", "-"))

        self.parent.myDB.updateDlState(episode_id, "1")

        ydl_opts = dict()
        ydl_opts["outtmpl"] = "{}_{}_S{}E{}.%(ext)s".format(show.replace(" ", "-"),
                                                            name.replace(" ", "-"),
                                                            season, episode)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        self.parent.myDB.removeEpisodeFromDL(episode_id)
        self.parent.myDB.updateEpisodeDlState(episode_id, "1")

        if not loc == self.dl_config["BASIC"]["defaultlocation"]:
            cmdline = self.dl_config["NETWORK"]["vpnstop"].split()
            proc = subprocess.Popen(cmdline,
                                    stdout=subprocess.PIPE)
