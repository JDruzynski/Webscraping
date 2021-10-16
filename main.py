from MiscFuncs import *
from AmazonClasses import *
from CraigslistClasses import *



def main():
    crawler = AmazonCrawler()
    listings = crawler.getListings("laptop", 2, {"Review":4})
    listPrint([crawler.getListingContent(i) for i in listings], 1)

if __name__ == "__main__":
    main()
