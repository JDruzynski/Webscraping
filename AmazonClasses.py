from GenericScraper import *
from GenericCrawler import *

class AmazonCrawler(GenericCrawler):
    """"""
    #
    baseUrl = "https://www.amazon.com"

    # Full or partial x-paths to website objects, used by selenium
    xpaths = {"search":'//*[@id="twotabsearchtextbox"]',
              "nextButton":'Next'}

    #Locations to be deconstructed in a find/find_all call by beautiful soup
    locations = {"listingCards" : ["div", {"data-asin" : True, "data-component-type": "s-search-result"}],
                 "listingTitle" : ["span", {"class":"a-size-medium a-color-base a-text-normal"}],
                 "listingURL" : ["a", {"class":"a-link-normal a-text-normal"}]}

    #Functions/lambdas for changing the page with refinements. Functions must take a driver as an argument
    refinements = {"Review":lambda driver, i: driver.find_elements_by_xpath('//*[@id="reviewsRefinements"]/ul/li')[4-i].click()}

    def __init__(self):
        super().__init__(self.AmazonPageScraper())

        self.driver.get(self.baseUrl)

    class AmazonPageScraper(Scraper):
        #Locations to be deconstructed in a find/find_all call by beautiful soup
        locations = {"Name" : ["span", {"id":"productTitle"}],
                     "Price" : ["span", {"id":"priceblock_ourprice"}],
                     "Overview" : ["div", {"id":"productOverview_feature_div"}],
                     "ProdFeatures" : ["div", {"id":"feature-bullets"}],
                     "Rating" : ["span", {"data-hook": "rating-out-of-text"}],
                     "Shipping" : ["div", {"id": "mir-layout-DELIVERY_BLOCK"}]}

        def __init__(self):
            super().__init__()

        def prettifiedScrape(self, soup:BeautifulSoup) -> dict:
            out = self._scrape(soup)

            out["Price"] = float(out["Price"].replace("$","").replace(",",""))

            out["Overview"] = {i.split("\n\n\n")[0].strip():i.split("\n\n\n")[1] for i in out["Overview"].split("\n\n\n\n")}

            out["ProdFeatures"] = [i.strip() for i in out["ProdFeatures"].split("\n\n\n")]

            return out

