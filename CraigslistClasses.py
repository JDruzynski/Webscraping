from GenericScraper import *
from GenericCrawler import *

class CraigslistCrawler(GenericCrawler):
    """"""
    #
    baseUrl = "https://sandiego.craigslist.org"

    # Full or partial x-paths to website objects, used by selenium
    xpaths = {"search":'//*[@id="query"]',
              "nextButton":'next'}

    #Locations to be deconstructed in a find/find_all call by beautiful soup
    locations = {"listingCards" : ["li", {"class" : "result-row"}],
                 "listingTitle" : ["a", {"class":"result-title hdrlnk"}],
                 "listingURL" : ["a", {"class":"result-title hdrlnk"}]}

    def __init__(self):
        super().__init__(self.CraigslistPageScraper())

        self.driver.get(self.baseUrl)

    class CraigslistPageScraper(Scraper):
        #Locations to be deconstructed in a find/find_all call by beautiful soup
        locations = {"Name" : ["span", {"id":"titletextonly"}],
                     "Price" : ["span", {"class":"price"}],
                     "Location" : ["small"],
                     "Description" : ["section", {"id":"postingbody"}],
                     "Attributes" : ["div", {"class":"mapAndAttrs"}]
                     }

        def __init__(self):
            super().__init__()

        def prettifiedScrape(self, soup:BeautifulSoup) -> dict:
            out = self._scrape(soup)

            return out

