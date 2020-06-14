# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import SelectorList
from fundmanager.items import Manager, Fund
import numpy
import logging
from scrapy_redis.spiders import RedisSpider


class ManagerSpider(RedisSpider):
    name = "manager"
    allowed_domains = ["fundf10.eastmoney.com","fund.eastmoney.com"]
    # start_urls = ['http://fundf10.eastmoney.com/jjjl_000256.html/']

    # def start_requests(self):
    #     res = requests.get("http://fund.eastmoney.com/js/fundcode_search.js")
    #     code_list = eval(res.content.decode('utf-8').split('=')[1][:-1])
    #     code_list = numpy.array(code_list)[:,0]
    #
    #     for i in tqdm(code_list):
    #         url = "http://fundf10.eastmoney.com/jjjl_{}.html".format(i)
    #         yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        manager_response = response.css('.jl_intro')
        funds_response = response.css('.jl_office')

        try:
            company = response.css('.bs_gl').xpath('./p/label/a[@href]/text()').extract()[-1]
        except Exception as e:
            return

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
            manager['url'] = 'http:' + manager_response[i].xpath('./a/@href').extract_first()
            img_url = manager_response[i].xpath('./a/img/@src').extract()
            if not 'http' in img_url[0]:
                img_url = ['http:' + img_url[0]]
            manager['image_urls'] = img_url
            manager['_id'] = manager['url'][-13:-5]

            try:
                funds_table = [[td.xpath('.//text()').extract_first() for td in tr.xpath('.//td')] for tr in funds_response[i].xpath('.//tbody//tr')]
                manager_name = funds_response[i].css('.jloff_tit a::text').extract_first()
            except Exception as e:
                logging.error("获取基金信息失败:{}".format(response.url))
                def parse_line(tr):
                    return [item.xpath('.//text()').extract_first() for item in tr.xpath('./td')]

                funds_table = numpy.array([parse_line(tr) for tr  in funds_response[i].xpath('./table/tbody/tr')])
                manager_name = funds_response[i].xpath('./div/label/a/text()').extract_first()

            manager['funds'] = numpy.array(funds_table)[:, 0].tolist()

            yield scrapy.Request(manager['url'],callback=self.parse_manager,meta={'manager':manager})

            for fund_list in funds_table:
                yield Fund(_id=manager['_id'] + '#' + fund_list[0],
                           code=fund_list[0],
                            name=fund_list[1],
                            type=fund_list[2],
                            start_date=fund_list[3],
                            end_date=fund_list[4],
                            duty_days=fund_list[5],
                            duty_return=fund_list[6],
                            average=fund_list[7],
                            rank=fund_list[8],
                            manager=manager_name,
                           company=company)

    def parse_manager(self,response):
        manager = response.meta['manager']
        info_list = response.xpath('//div[@class="right jd "]').xpath('.//text()').extract()
        info_list = [i.strip() for i in info_list if i.strip()]
        manager['appointment_date'] = info_list[3]
        manager['company'] = info_list[5]
        manager['fund_asset_size'] = ''.join(response.xpath('//div[@class="right jd "]//span[@class="numtext"]')[0].xpath('.//text()').extract())
        manager['best_return'] = ''.join(response.xpath('//div[@class="right jd "]//span[@class="numtext"]')[1].xpath('.//text()').extract())
        yield manager