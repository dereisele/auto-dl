import scrappertools
import re
import json
from bs4 import BeautifulSoup
import requests

class Scrapper(scrappertools.BasicScrapper):
    BASE_URL = "http://www.dmax.de"

    def setup(self, app):
        print("setup dmax")
        self.parent = app
        self.parent.register_scrapper('de_dmax_de', self.scrap)

    def scrap(self):
        r = requests.get(self.BASE_URL + "/videos/#dni-listing2143929440-alle")
        bs = BeautifulSoup(r.text, "html.parser")

        shows_raw = bs.find("script", text=re.compile("\(function \(window\) {\n(.|\n)+")).string

        # TODO: Use RE!!!
        shows = shows_raw.split("ta = ")[1].split("if (typeof")[0].strip().rstrip(";")

        j_shows = json.loads(shows)["raw"]
        for s in j_shows:
            myTVShowTitle = s["title"].rstrip(" - VIDEOS")
            url = s["url"]
            #print(url)
            self.parent.myDB.addShow(myTVShowTitle, "de")
            myShowID = self.parent.myDB.getShowID(myTVShowTitle, "de")
            print(myShowID)

            r = requests.get(url)
            bs = BeautifulSoup(r.text, "html.parser")
            seasons_raw = bs.find_all("div", class_="tab-module-header")

            for sr in seasons_raw:
                seasonNumber_raw = sr.string

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

                        episodes = bs.find("div", class_="episode-list").find_all("a")
                        for e in episodes:
                            url = e["href"]
                            episodeNumber = e.span.h3.string.lstrip("Episode ")
                            #print(episodeNumber)
                            myEpisodeTitle = e.span.h3.next_sibling.string
                            self.parent.myDB.addEpisode(myShowID,
                                                        seasonNumber,
                                                        episodeNumber,
                                                        myEpisodeTitle,
                                                        url, "de", "unknown")

                    except:
                        print("Skip episode")
