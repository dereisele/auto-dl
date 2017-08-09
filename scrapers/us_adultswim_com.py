import scrapertools
import re
import json
from bs4 import BeautifulSoup
import requests

class Scraper(scrapertools.BasicScraper):
    BASE_URL = "http://www.adultswim.com"

    def setup(self, app):
        print("setup adultswim")
        self.parent = app
        self.parent.register_scraper('us_adultswim_com', self.scrape)

    def scrape(self):
        r = requests.get(self.BASE_URL + "/videos/")
        bs = BeautifulSoup(r.text, "html.parser")

        shows_raw = bs.find("script", text=re.compile("__AS_INITIAL_DATA__(.)+")).string
        shows_raw = shows_raw.strip().lstrip("__AS_INITIAL_DATA__ = ").rstrip(";")
        #print(shows_raw)

        j_shows = json.loads(shows_raw)

        for s in j_shows["shows"]:
            myTVShowTitle = s["title"]

            self.parent.myDB.addShow(myTVShowTitle, "en")
            myShowID = self.parent.myDB.getShowID(myTVShowTitle, "en")

            show_url = self.BASE_URL + s["url"]

            r = requests.get(show_url)
            bs = BeautifulSoup(r.text, "html.parser")

            episodes_raw_bs = bs.find("script", text=re.compile("__AS_INITIAL_DATA__(.)+"))

            # Filters shows without episodes
            if episodes_raw_bs is None:
                continue
            episodes_raw = episodes_raw_bs.string
            episodes_raw = episodes_raw.strip().lstrip("__AS_INITIAL_DATA__ = ").rstrip(";")
            #print(shows_raw)

            j_episodes = json.loads(episodes_raw)

            # Filters livestreams
            if "show" not in j_episodes:
                continue
            print(myTVShowTitle)

            for e in j_episodes["show"]["videos"]:

                # Filters episodes, which require login
                if e["auth"]:
                    continue

                seasonNumber = e["season_number"] if e["season_number"] != "" else "0"
                episodeNumber = e["episode_number"] if e["episode_number"] != "" else "0"
                myEpisodeTitle = e["title"]
                url = show_url + "/" + e["slug"]

                self.parent.myDB.addEpisode(myShowID,
                                            seasonNumber,
                                            episodeNumber,
                                            myEpisodeTitle,
                                            url, "us", "unknown")
                #print("  ", seasonNumber, "E", episodeNumber)
