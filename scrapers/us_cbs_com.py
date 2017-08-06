import scrapertools
import re
import json
from bs4 import BeautifulSoup
import requests

class Scraper(scrapertools.BasicScraper):
    BASE_URL = "http://www.cbs.com"

    def setup(self, app):
        print("setup cbs")
        self.parent = app
        self.parent.register_scraper('us_cbs_com', self.scrape)

    def scrape(self):
        r = requests.get(self.BASE_URL + "/shows")
        bs = BeautifulSoup(r.text, "html.parser")

        shows = bs.find_all("li", class_="showPosterWrapper")

        url_episode = "http://www.cbs.com/carousels/videosBySection/{id}/offset/{offset}/limit/{limit}/xs/0/10/"

        for s in shows:
            myTVShowTitle = s.div.div.next_sibling.next_sibling.string
            url = s.div.div.a["href"]
            self.parent.myDB.addShow(myTVShowTitle, "en")
            myShowID = self.parent.myDB.getShowID(myTVShowTitle, "en")

            r = requests.get(self.BASE_URL + url + "video")
            bs = BeautifulSoup(r.text, "html.parser")

            # CBS Api
            carousels = bs.find_all("div", id=re.compile("id-carousel-[0-9]+"))

            for c in carousels:
                self.limit = 25
                self.offset = 0

                self.done = False

                while not self.done:
                    print(" " + str(self.offset))
                    r = requests.get(url_episode.format(limit=self.limit,
                                                        offset=self.offset,
                                                        id=c["id"].lstrip("id-carousel-")))
                    j_episodes = json.loads(r.text)

                    print("  test success")
                    if j_episodes["success"]:
                        print("    X")
                        self.total = j_episodes["result"]["total"]

                        print("  test full episode")
                        if j_episodes["result"]["title"] == "Full Episodes":
                            print("    X")
                            for j_e in j_episodes["result"]["data"]:

                                myEpisodeTitle = j_e["episode_title"]
                                seasonNumber = j_e["season_number"]
                                episodeNumber = j_e["episode_number"]
                                url = self.BASE_URL + j_e["url"]

                                self.parent.myDB.addEpisode(myShowID,
                                                            seasonNumber,
                                                            episodeNumber,
                                                            myEpisodeTitle,
                                                            url, "us",
                                                            "unknown")
                            print("  test total")

                            self.done = (self.offset + self.limit) >= self.total
                            self.offset += 25
                        else:
                            self.done = True
                    else:
                        self.done = True
