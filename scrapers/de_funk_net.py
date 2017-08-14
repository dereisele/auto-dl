import re
from bs4 import BeautifulSoup
import requests
from scrapertemplates import basic


class Scraper(basic.BasicScraper):

    SCRAPER_ID = __name__
    BASE_URL = "http://www.funk.net"

    def identify_show(self, name):
        """Translate messy show name to standard names."""
        name_old = name
        name = re.sub(" - Staffel [1-9]", "", name)
        name = name.rstrip(" (OV)")
        name = name.rstrip(" - OV")
        name = name.rstrip(" -")
        print("{}->{}".format(name_old, name))
        return name.strip()

    def identify_episode(self, name):
        """Translate messy episode name to standard name."""
        name_old = name
        name = re.sub("(([A-Z]){2,} FINALE I )|(I ([A-Z]){2,})|(( I )*Staffel (\d)+)|( (Folge|FOLGE|Episode)+ (\d)+)|(( I )* in 4K)|( \(OV\))|( - OV)", "", name)
        print("{}->{}".format(name_old, name.strip()))
        return name.strip()

    def scrape(self):
        """Scrape Funk.net (Germany)."""
        print("    /FUNK")
        r = requests.get(self.BASE_URL + "/serien")
        bs = BeautifulSoup(r.text, "html.parser")

        shows = [s for s in bs.find_all("div", class_="slide-inner")]
        #print(shows[0])
        for s in shows:
            myTVShowTitle = s.a["title"].rstrip(" | funk")

            OV = myTVShowTitle.endswith(" (OV)") or myTVShowTitle.endswith("OV")

            myTVShowTitle = self.identify_show(myTVShowTitle)

            lang = self.getOVLang(myTVShowTitle) if OV else "de"

            self.parent.myDB.addShow(myTVShowTitle, lang)
            myShowID = self.parent.myDB.getShowID(myTVShowTitle, lang)

            r = requests.get(self.BASE_URL + s.a["href"])
            bs = BeautifulSoup(r.text, "html.parser")

            currentEpisodes = [e for e in bs.findAll("div", class_="show-more-item")]

            for e in currentEpisodes:
                url = self.BASE_URL + e.a["href"]
                number_raw = e.a.div.p.text
                seasonNumber = number_raw.split(" • ")[0].lstrip("Staffel ")
                episodeNumber = number_raw.split(" • ")[1].lstrip("Episode ")
                myEpisodeTitle = e.a["title"].split(" | ")[0]
                quality = "unknown"
                if myEpisodeTitle.endswith("in 4K"):
                    quality = "4K"
                myEpisodeTitle = self.identify_episode(myEpisodeTitle)

                self.parent.myDB.addEpisode(myShowID, seasonNumber,
                                            episodeNumber, myEpisodeTitle,
                                            url, "de", quality)
