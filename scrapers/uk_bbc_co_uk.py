import re
from bs4 import BeautifulSoup
import string
import requests

from scrapertemplates import basic


class Scraper(basic.BasicScraper):
    """Scraper for bbc.co.uk/iplayer (UK)."""

    SCRAPER_ID = __name__
    BASE_URL = "http://www.bbc.co.uk"
    PROGRAMME_URL = BASE_URL + "/programmes/{id}/episodes/player"

    def scrape(self):
        """Scrape bbc.co.uk (UK)."""
        letters = list(string.ascii_lowercase)

        # Add "0-9" to list of letters for alphabetic show list
        letters.append("0-9")

        # TODO
        return

        for l in letters:
            r = requests.get(self.BASE_URL + "/iplayer/a-z/" + l)
            bs = BeautifulSoup(r.text, "html.parser")
            for column in bs.find_all("ol", class_="tleo-list"):
                for show_bs in column.find_all("li"):

                    pID = show_bs.a["href"].split("/")[-1]  # BBC programme id
                    myShowTitle = show_bs.a.span.string

                    url = self.PROGRAMME_URL.format(id=pID)

                    r = requests.get(url)

                    bs = BeautifulSoup(r.text, "html.parser")
                    channel = "TODO"
                    if channel == "S4C":
                        lang = "cy"  # Welsh
                    elif channel == "BBC Alba":
                        lang = "gd"  # Scottish Gaelic
                    else:
                        lang = "en"

                    myShowID = self.addShow(myShowTitle, lang)
                    print(bs.head.title.string)
                    if "CBBC" in str(bs.head.title.string) or "CBeebies" in str(bs.head.title.string):
                        # TODO: Add CBBC
                        print("Skip")
                        continue

                    episodes_bs = bs.find("ol", class_="highlight-box-wrapper")
                    if episodes_bs is not None:
                        print(len(episodes_bs))

                    for e in episodes_bs:
                        url = e.div["resource"]



if __name__ == "__main__":
    Scraper().scrape()
