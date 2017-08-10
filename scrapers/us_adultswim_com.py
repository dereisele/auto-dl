"""Scraper for adultswim.com (USA)."""
import scrapertools
import re
import json
from bs4 import BeautifulSoup
import requests


class Scraper(scrapertools.BasicScraper):
    """Basic Scraper for adultswim.com (USA)."""

    BASE_URL = "http://www.adultswim.com"

    def setup(self, app):
        """Setup adultswim.com sraper."""
        print("setup adultswim")
        self.parent = app
        self.parent.register_scraper('us_adultswim_com', self.scrape)

    def scrape(self):
        """Scrape adultswim.com."""
        r = requests.get(self.BASE_URL + "/videos/")
        bs = BeautifulSoup(r.text, "html.parser")

        shows_raw = bs.find("script",
                            text=re.compile("__AS_INITIAL_DATA__(.)+")).string
        shows_raw = shows_raw.strip()
        shows_raw = shows_raw.lstrip("__AS_INITIAL_DATA__ = ").rstrip(";")

        j_shows = json.loads(shows_raw)

        for s in j_shows["shows"]:
            myTVShowTitle = s["title"]

            self.parent.myDB.addShow(myTVShowTitle, "en")
            myShowID = self.parent.myDB.getShowID(myTVShowTitle, "en")

            show_url = self.BASE_URL + s["url"]

            r = requests.get(show_url)
            bs = BeautifulSoup(r.text, "html.parser")

            episodes_bs = bs.find("script",
                                  text=re.compile("__AS_INITIAL_DATA__(.)+"))

            # Filters shows without episodes
            if episodes_bs is None:
                continue
            episodes_raw = episodes_bs.string
            episodes_raw = episodes_raw.strip().rstrip(";")
            episodes_raw = episodes_raw.lstrip("__AS_INITIAL_DATA__ = ")

            j_episodes = json.loads(episodes_raw)

            # Filters livestreams
            if "show" not in j_episodes:
                continue
            print(myTVShowTitle)

            for e in j_episodes["show"]["videos"]:

                # Filters episodes, which require login
                print(e["auth"])
                if e["auth"]:
                    continue

                # Filter clips
                if e["season_number"] != "":
                    seasonNumber = e["season_number"]
                else:
                    continue

                if e["episode_number"] != "":
                    episodeNumber = e["episode_number"]
                else:
                    continue

                myEpisodeTitle = e["title"]
                url = show_url + e["slug"]

                self.parent.myDB.addEpisode(myShowID,
                                            seasonNumber,
                                            episodeNumber,
                                            myEpisodeTitle,
                                            url, "us", "unknown")
                print("Inserted")
