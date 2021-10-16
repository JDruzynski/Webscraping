import abc
from abc import ABC, abstractmethod
import typing
from bs4 import BeautifulSoup

class Scraper(ABC):
    #Locations to be deconstructed in a find/find_all call by beautiful soup
    locations = {}

    def _scrape(self, soup:BeautifulSoup) -> dict:
        out = {}
        for name, loc in self.locations.items():
            if (x := soup.find(*loc)):
                out[name] = x.text.strip()
        return out

    @abstractmethod
    def prettifiedScrape(self, soup:BeautifulSoup) -> dict:
        pass



