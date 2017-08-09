"""Scraper for dmax.de (DE)."""
import scrapertools
import re
import json
from bs4 import BeautifulSoup
import requests


class Scraper(scrapertools.BasicScraper):
    """Basic Scraper for dmax.de (DE)."""

    BASE_URL = "http://www.dmax.de"

    def setup(self, app):
        """Setup dmax.de sraper."""
        print("setup dmax")
        self.parent = app
        self.parent.register_scraper('de_dmax_de', self.scrape)

    def scrape(self):
        """Scrape dmax.de."""
        r = requests.get(self.BASE_URL + "/videos/#dni-listing2143929440-alle")
        bs = BeautifulSoup(r.text, "html.parser")

        p = re.compile("\(function \(window\) {\n(.|\n)+")
        shows_raw = bs.find("script", text=p).string

        shows_raw = shows_raw.split("ta = ")[1]
        shows_raw = shows_raw.split("if (typeof")[0]
        shows = shows_raw.strip().rstrip(";")

        j_shows = json.loads(shows)["raw"]
        for s in j_shows:
            myTVShowTitle = s["title"].rstrip(" - VIDEOS")
            url = s["url"]
            self.parent.myDB.addShow(myTVShowTitle, "de")
            myShowID = self.parent.myDB.getShowID(myTVShowTitle, "de")
            print(myShowID)

            r = requests.get(url)
            bs = BeautifulSoup(r.text, "html.parser")
            seasons_raw = bs.find_all("div", class_="tab-module-header")

            for sr in seasons_raw:
                seasonNumber_raw = sr.string
                seasonNumber_raw = seasonNumber_raw.lstrip("NEU - ")

                seasonNumber = False

                if seasonNumber_raw == "GANZE FOLGEN":
                    seasonNumber = "0"
                if seasonNumber_raw.startswith("STAFFEL "):
                    seasonNumber = seasonNumber_raw.lstrip("STAFFEL ")

                if seasonNumber:
                    print("Bing.")
                    try:
                        url_firstvideo = sr.next_sibling()[0].find("a")["href"]

                        r = requests.get(url_firstvideo)
                        bs = BeautifulSoup(r.text, "html.parser")

                        episodes = bs.find("div", class_="episode-list")
                        episodes = episodes.find_all("a")

                        for e in episodes:
                            url = e["href"]
                            episodeNumber = e.span.h3.string.lstrip("Episode ")
                            myEpisodeTitle = e.span.h3.next_sibling.string
                            self.parent.myDB.addEpisode(myShowID,
                                                        seasonNumber,
                                                        episodeNumber,
                                                        myEpisodeTitle,
                                                        url, "de", "unknown")

                    except Exception:
                        print("Skip episode")
