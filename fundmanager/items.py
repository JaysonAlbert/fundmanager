# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Manager(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    appointment_date = scrapy.Field()
    introduction = scrapy.Field()
    company = scrapy.Field()
    fund_asset_size = scrapy.Field()
    sex = scrapy.Field()
    funds = scrapy.Field()
    best_return = scrapy.Field()

    image_urls = scrapy.Field()
    picture = scrapy.Field()


class Fund(scrapy.Item):
    _id = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    duty_days = scrapy.Field()
    duty_return = scrapy.Field()
    average = scrapy.Field()
    rank = scrapy.Field()
    manager = scrapy.Field()
