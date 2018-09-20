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

    @staticmethod
    def get_collection_name():
        return 'manager'


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
    company = scrapy.Field()

    @staticmethod
    def get_collection_name():
        return 'fund'


class Company(scrapy.Item):
    _id = scrapy.Field()
    short_name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    asset_size = scrapy.Field()
    fund_num = scrapy.Field()
    manager_num = scrapy.Field()
    establishment_date = scrapy.Field()
    company_nature = scrapy.Field()
    east_money_rank = scrapy.Field()
    location = scrapy.Field()
    manager = scrapy.Field()
    website = scrapy.Field()
    phone = scrapy.Field()

    @staticmethod
    def get_collection_name():
        return 'company'


class FundScale(scrapy.Item):
    _id = scrapy.Field()
    company = scrapy.Field()
    fund_type = scrapy.Field()
    x = scrapy.Field()
    y = scrapy.Field()

    @staticmethod
    def get_collection_name():
        return 'scale'


FUNDTYPE = {
    '11': 'index',
    '25': 'stock',
    '27': 'hybrid',
    '31': 'bond',
    '35': 'currency',
    '36': 'investment_product',
    '37': 'qdii',
    '38': 'capital_preservation',
}
