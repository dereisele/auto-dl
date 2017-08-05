import scrappertools
from bs4 import BeautifulSoup
import re
import requests
import json

class DiscoveryScrapper(scrappertools.BasicScrapper):
    """Scrapper Template for DiscoveryGo (USA)."""

    CHANNEL = ""

    token = ""
    codes = {"sciencechannel": "SCI",
             "discovery": "DSC",
             "animalplanet": "APL",
             "investigationdiscovery": "IDS",
             "velocity": "VEL",
             "destinationamerica": "DAM",
             "ahctv": "AHC",
             "discoverylife": "DLF",
             "tlc": "TLC"}

    def scrap(self):
        """Scrap Discovery networks (USA)."""
        for s in self.getShows():
            print(s[0])
            self.getEpisodes(s)

    def getShows(self):
        url_token = "https://www.{channel}.com/anonymous?authLink=https%3A%2F%2Flogin.discovery.com%2Fv1%2Foauth2%2Fauthorize%3Fclient_id%3D3020a40c2356a645b4b4%26redirect_uri%3Dhttps%253A%252F%252Ffusion.ddmcdn.com%252Fapp%252Fmercury-sdk%252F180%252FredirectHandler.html%253Fhttps%253A%252F%252Fwww.{channel}.com%26response_type%3Danonymous%26state%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJub25jZSI6InFIYmVsMjF3dGZLZTRZRnhpZFdIOVdoSElPQ0Y1R2E2In0.nbxy_qf3PyWErA7FwFkh1XtaDSpLkuJlfILQM_s34mE%26networks.code%3DSCI&client_id=3020a40c2356a645b4b4&state=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJub25jZSI6InFIYmVsMjF3dGZLZTRZRnhpZFdIOVdoSElPQ0Y1R2E2In0.nbxy_qf3PyWErA7FwFkh1XtaDSpLkuJlfILQM_s34mE".format(channel=self.CHANNEL)

        url_shows = "https://api.discovery.com/v1/content/shows?networks.code={code}&platform=desktop&product=sites&sort=-video.airDate.type%28episode%7Climited%7Cevent%7Cstunt%7Cextra%29".format(code=self.codes[self.CHANNEL])

        r = requests.get(url=url_token)
        self.token = json.loads(r.text)["access_token"]

        r = requests.get(url=url_shows,
                         headers={"authorization": "Bearer " + self.token})
        j_shows = json.loads(r.text)
        for show in j_shows:
            yield (show["name"], show["socialUrl"].split("/")[3])

    def getEpisodes(self, show):
        ch = self.CHANNEL
        if ch == "velocity":
            ch += "channel"

        url_episodes = "https://www.{channel}go.com/{show_link}/".format(channel=ch, show_link=show[1])

        print(url_episodes)

        myTVShowTitle = show[0]

        self.parent.myDB.addShow(myTVShowTitle, "en")
        myShowID = self.parent.myDB.getShowID(myTVShowTitle, "en")

        r = requests.get(url_episodes)
        bs = BeautifulSoup(r.text, "html.parser")

        episodeInfos = [e for e in bs.find_all("script", type="application/ld+json")]
        #print(episodeInfos)
        for eI in episodeInfos:

            #Are these mistakes in js for any purpose
            b = """}
        }
    }"""
            text = eI.string
            text = text.replace(b, "}}")
            text = re.sub("(&.+;)", "", text)
            text = text.replace("\"sameAs :", "\"sameAs\" :")
            text = re.sub("\r|\n", "", text)
            js = json.loads(text)

            if js["@type"] == "TVEpisode":
                Free = not eI.next_sibling.next_sibling.next_sibling.next_sibling.div["class"][0] == "content-auth"
                #print(eI.next_sibling.next_sibling.next_sibling.next_sibling.div["class"][0])

                if Free:
                    print("FREE PREVIEW")
                        #print(js)
                        #print("--------------------------------------------")
                    try:
                        episodeNumber = js["episodeNumber"]
                        seasonNumber = 0
                        myEpisodeTitle = js["name"]
                        quality = "1080"
                        url = js["sameAs"]
                        seasonNumber = js["partOfSeason"]["seasonNumber"]

                        self.parent.myDB.addEpisode(myShowID,
                                                    seasonNumber,
                                                    episodeNumber,
                                                    myEpisodeTitle,
                                                    url, "us", quality)
                    except:
                        print("Skip episode")
