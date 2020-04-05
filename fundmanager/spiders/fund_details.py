# -*- coding: utf-8 -*-
import scrapy
from fundmanager.spiders.utils import code_list
import numpy as np
from fundmanager.items import FundAssets, Errors


def get_shares(data):
    return sum([float(i.replace('%', '')) for i in data[:, -3] if i != '---'])


def get_market_value(data):
    return sum([float(i.replace(',', '')) for i in data[:, -1] if i != '---'])


class FundDetailsSpider(scrapy.Spider):
    name = "fund-details"
    allowed_domains = ["fundf10.eastmoney.com","fund.eastmoney.com"]
    start_urls = ['http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=070002&topline=10&year=2017']
    url_format = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year={}"
    start_year = "2019" # 起始年份

    def start_requests(self):
        fund_codes = code_list()

        for code in fund_codes:
            url = self.url_format.format(code, self.start_year)
            yield scrapy.Request(url, callback=self.parse, meta={'code': code,'date': self.start_year, 'recurse': True})

        # for url in self.start_urls:
        #     yield scrapy.Request(url, callback=self.parse, meta={'code':'070002','date': self.start_year, 'recurse': True})


    def parse(self, response):
        code = response.meta['code']
        cur_date = response.meta['date']

        for box in response.css("div.box"):
            publish_date = box.css('label>font.px12::text').extract_first()
            try:
                data = np.array([row.css('td:not([class^="xglj"]) *::text').extract() for row in box.css('tbody > tr')])
                data = np.concatenate((data[:,1:3],data[:,-3:]), axis=1)

                asset = FundAssets()
                asset['_id'] = code + '#' + publish_date
                asset['code'] = code
                asset['published_date'] = publish_date
                asset['funds'] = data.tolist()
                asset['head_shares'] = get_shares(data)
                asset['head_market_value'] = get_market_value(data)
                asset['market_value'] = asset['head_market_value'] / asset['head_shares'] if asset['head_shares'] != 0 else 0

                yield asset

                # 如果需要爬取子页面
                if response.meta['recurse']:
                    try:
                        for date in ''.join(response.xpath("//body/text()").extract()).split('[')[1].split(']')[0].split(','):
                            if cur_date == date:
                                continue
                            url = self.url_format.format(response.meta['code'], date)
                            yield scrapy.Request(url, callback=self.parse, meta={'code': code, 'date': date, 'recurse': False})
                    except Exception as e:
                        error = Errors()
                        error['_id'] = response.url
                        error['name'] = self.name
                        yield error
            except ValueError as e:
                error = Errors()
                error['_id'] = response.url
                error['name'] = self.name
                yield error
