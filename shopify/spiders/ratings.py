import scrapy
import re
import datetime

from shopify.cache import RatingsCache
from shopify.items import ShopifyItem
from shopify.util import remove_url_parameters


class RatingsSpider(scrapy.Spider):
    name = 'shopify_ratings_spider'
    start_urls = [
        'https://apps.shopify.com/browse/all?page=1&pricing=all&requirements=off&sort_by=installed',
    ]

    def parse(self, response):
        self.logger.info("Visited %s", response.url)
        cache = RatingsCache()
        # follow links to app pages
        for app_link in response.css('div.ui-app-card a'):
            app_url = remove_url_parameters(app_link.attrib['href'])
            if cache.was_scraped(app_url):
                self.logger.info('App %s was already scrapped. Skipping...' % app_url)
                continue
            yield response.follow(app_link, callback=self.parse_app)

        # follow links to next page extracted from pagination section
        for page in response.css('div.search-pagination.hide--mobile').css('a.search-pagination__next-page-text'):
            yield response.follow(page, callback=self.parse)

    def parse_app(self, response):
        self.logger.info("Visited %s", response.url)

        item = ShopifyItem()
        item['name'] = response.css('.ui-app-store-hero__header__app-name::text').get()
        item['url'] = remove_url_parameters(response.url)
        item['overall_rating'] = response.css('.ui-star-rating__rating::text').get()
        item['visit_date'] = datetime.datetime.utcnow().isoformat()

        # initialize all ratings with zero, so the spider fill only the voted ones
        for i in range(1, 6):
            item['ratings_%s' % i] = 0

        for review in response.css('.reviews-summary__review-count'):
            review_url = review.css('a::attr("href")').get()  # ex: facebook-store/reviews?rating=5
            review_quantity = review.css('a::text').get()  # ex: (138)
            if not review_url or not review_quantity:
                # no one rated this value, so go to the next
                continue

            rating_search = re.search('.*rating=(\\d+)', review_url, re.IGNORECASE)
            rating = rating_search.group(1)
            item['ratings_%s' % rating] = review_quantity.strip("()")

        yield item
