import csv

from shopify.singleton import Singleton
from shopify.util import remove_url_parameters


class RatingsCache(metaclass=Singleton):
    def __init__(self, data_file="shopify.csv"):
        self.data_file = data_file
        self.cache = set()
        self.load_cache()

    def load_cache(self):
        with open(self.data_file) as ratings_file:
            reader = csv.DictReader(ratings_file)
            for row in reader:
                self.cache.add(row['url'])

    def was_scraped(self, url):
        clean_url = remove_url_parameters(url)
        return clean_url in self.cache
