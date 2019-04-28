# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EbayCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()  # Ads ID
    model = scrapy.Field()  # Model of Refrigerator
    brand = scrapy.Field()  # Manufacturer
    url = scrapy.Field()  # ads url
    condition = scrapy.Field()  # brand new(buy it now)/used
    location = scrapy.Field()  # location of the ads
    delivery_time = scrapy.Field()  # حestimated delivery time
    price = scrapy.Field()  # price of the item
    capacity = scrapy.Field()  # Description
