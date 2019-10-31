# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopifyItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    overall_rating = scrapy.Field()
    ratings_5 = scrapy.Field()
    ratings_4 = scrapy.Field()
    ratings_3 = scrapy.Field()
    ratings_2 = scrapy.Field()
    ratings_1 = scrapy.Field()
    visit_date = scrapy.Field()
