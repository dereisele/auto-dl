"""Scraper for cbs.com (USA)."""
import scrapertools
import re
import json
from bs4 import BeautifulSoup
import requests


class Scraper(scrapertools.BasicScraper):
    """Basic Scraper for cbs.com (USA)."""

    BASE_URL = "http://www.cbs.com"

    def setup(self, app):
        """Setup cbs.com sraper."""
        print("setup cbs")
        self.parent = app
        self.parent.register_scraper('us_cbs_com', self.scrape)

    def scrape(self):
        """Scrape cbs.com."""
        r = requests.get(self.BASE_URL + "/shows")
        bs = BeautifulSoup(r.text, "html.parser")

        shows = bs.find_all("li", class_="showPosterWrapper")

        url_episode = "http://www.cbs.com/carousels/videosBySection/{id}"
        url_episode += "/offset/{offset}/limit/{limit}/xs/0/10/"

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
                limit = 25
                offset = 0
                total = 42  # 42 as placeholder
                cID = c["id"].lstrip("id-carousel-")
                done = False

                while not done:
                    print(" " + str(offset))
                    r = requests.get(url_episode.format(limit=limit,
                                                        offset=offset,
                                                        id=cID))
                    j_episodes = json.loads(r.text)

                    print("  test success")
                    if j_episodes["success"]:
                        print("    X")
                        total = j_episodes["result"]["total"]

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
                                                            "720")
                            print("  test total")

                            done = (offset + limit) >= total
                            offset += 25
                        else:
                            done = True
                    else:
                        done = True
