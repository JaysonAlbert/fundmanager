# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import SelectorList
from scrapy.shell import inspect_response
from fundmanager.items import Manager, Fund
import numpy
import requests


class ManagerSpider(scrapy.Spider):
    name = "manager"
    allowed_domains = ["http://fundf10.eastmoney.com"]
    start_urls = ['http://fundf10.eastmoney.com/jjjl_000256.html/']

    def start_requests(self):
        res = requests.get("http://fund.eastmoney.com/js/fundcode_search.js")
        code_list = eval(res.content.decode('utf-8').split('=')[1][:-1])
        code_list = numpy.array(code_list)[:,0]

        for i in code_list:
            url = "http://fundf10.eastmoney.com/jjjl_{}.html".format(i)
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        manager_response = response.css('.jl_intro')
        funds_response = response.css('.jl_office')

        num = len(manager_response)
        if isinstance(manager_response,SelectorList):
            assert num == len(funds_response)
        else:
            manager_response = [manager_response]
            funds_response = [funds_response]

        for i in range(num):
            manager = Manager()
            intro_list = manager_response[i].xpath('.//text()').extract()
            manager['name'] = intro_list[1]
            manager['appointment_date'] = intro_list[3]
            manager['introduction'] = intro_list[4]

            try:
                funds_table_list = funds_response[i].xpath('.//text()').extract()
                funds_table = numpy.array(funds_table_list[2:]).reshape(-1, 9)
                manager_name = funds_table_list[0]
            except Exception:
                # funds_table_list = []
                # for tr in funds_response[i].xpath('./table/tbody/tr'):
                #     row = [item.xpath('.//text()').extract_first() for item in tr.xpath('./td')]
                def parse_line(tr):
                    return [item.xpath('.//text()').extract_first() for item in tr.xpath('./td')]

                funds_table = numpy.array([parse_line(tr) for tr  in funds_response[i].xpath('./table/tbody/tr')])
                manager_name = funds_response[0].xpath('./div/label/a/text()').extract_first()

            yield manager

            manager['funds'] = funds_table[1:, 0].tolist()

            for fund_list in funds_table[1:,]:
                yield Fund(code=fund_list[0],
                            name=fund_list[1],
                            type=fund_list[2],
                            start_date=fund_list[3],
                            end_date=fund_list[4],
                            duty_days=fund_list[5],
                            duty_return=fund_list[6],
                            average=fund_list[7],
                            rank=fund_list[8],
                            manager=manager_name)
