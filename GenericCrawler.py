from GenericScraper import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import typing
from typing import TypedDict, List

"""Set up Types"""
class Listing(TypedDict):
    itemTag:str
    url:str

Listings = List[Listing]


class GenericCrawler:
    """Class that creates a chrome window and """
    chromedriverPath = "C:\\Users\\jarre\\PycharmProjects\\WebScraing\\chromedriver.exe"
    baseUrl = ""
    driver:webdriver.Chrome

    # Full or partial x-paths to website objects, used by selenium
    xpaths = {"search":'',
              "nextButton":""}

    #Locations to be deconstructed in a find/find_all call by beautiful soup
    locations = {"listingCards" : [],
                 "listingTitle" : [],
                 "listingURL" : []}

    #Functions/lambdas for changing the page with refinements. Functions must take a driver as an argument
    refinements = {}

    def __init__(self, scraper:Scraper):
        self.scraper = scraper
        self.driver = webdriver.Chrome(executable_path=self.chromedriverPath)

    def getListings(self, searchItem:str, numReturn:int, searchCriteria:dict = {}) -> Listings:
        """Get list with specified number of results and their links"""
        soup = self.searchItem(searchItem, searchCriteria)
        cards = soup.find_all(*self.locations["listingCards"])
        while len(cards) < numReturn:
            soup = self.nextPage()
            cs = soup.find_all(*self.locations["listingCards"])
            cards += [*cs]

        out = []
        for card in cards:
            if (t := card.find(*self.locations["listingTitle"])) and (u := card.find(*self.locations["listingURL"])):
                out += [Listing(itemTag = t.text, url = u.get("href"))]

        return out[:numReturn]

    def searchItem(self, searchItem:str, searchCriteria:dict = {}) -> BeautifulSoup:
        #Search for item in search bar
        self.driver.find_element_by_xpath(self.xpaths["search"]).send_keys(searchItem)
        self.driver.find_element_by_xpath(self.xpaths["search"]).send_keys(Keys.RETURN)

        self.refineSearch(searchCriteria)

        content = self.driver.page_source

        return BeautifulSoup(content, "lxml")

    def refineSearch(self, searchCriteria:dict = {}):
        if not searchCriteria: return

        for criteria, value in searchCriteria.items():
            if criteria in self.refinements:
                self.refinements[criteria](self.driver, value)

    def nextPage(self) -> BeautifulSoup:
        #Click onnext button
        link = WebDriverWait(self.driver,15).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, self.xpaths["nextButton"])))
        link.click()
        self.driver.refresh()
        content = self.driver.page_source

        return BeautifulSoup(content, "lxml")

    def getListingContent(self, listing:Listing):
        """Uses scraper to scrape the required content from the page and returns it"""
        if self.baseUrl in listing["url"]:
            url = listing["url"]
        else:
            url = self.baseUrl + listing["url"]

        self.driver.get(url)

        content = self.driver.page_source

        soup =  BeautifulSoup(content, "lxml")

        out = self.scraper.prettifiedScrape(soup)
        out["url"] = url
        return out

    def __del__(self):
        self.driver.quit()
