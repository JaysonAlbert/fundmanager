import scrapy
from scrapy.shell import inspect_response


from fundmanager.items import Company, FundScale, FUNDTYPE
import functools
import requests


class CompanySpider(scrapy.Spider):
    name = 'company'

    allowed_domains = ["fundf10.eastmoney.com", "fund.eastmoney.com"]
    start_urls = ['http://fund.eastmoney.com/company/default.html']

    def parse(self, response):
        list_item = response.css('.sencond-block').xpath('./a[@href]')
        for item in list_item:
            company = Company()
            company['url'] = response.urljoin(item.xpath('./@href').extract_first())
            company['short_name'] = item.xpath('./text()').extract_first()
            yield scrapy.Request(company['url'], functools.partial(self.parse_details, company))

    def parse_details(self, company, response):
        basic_info = response.css('.common-basic-info')
        company['_id'] = response.url.split('/')[-1].split('.')[0]
        company['name'] = basic_info.xpath('./div[1]/div[1]/p[1]/text()').extract_first()
        info_list = basic_info.css('.grey *::text').extract()
        if len(info_list) == 11:
            company['location'] = info_list[0]
            company['manager'] = info_list[1]
            company['website'] = info_list[2]
            company['phone'] = info_list[3]
            company['asset_size'] = info_list[4]
            company['fund_num'] = info_list[5]
            company['manager_num'] = info_list[7]
            company['establishment_date'] = info_list[9]
            company['company_nature'] = info_list[10]
        else:  # 数据缺失
            firm_contact = basic_info.css('.firm-contact .grey *::text').extract()
            if len(firm_contact) != 0:
                company['location'] = firm_contact[0]
                company['manager'] = firm_contact[1]
                company['website'] = firm_contact[2]
                company['phone'] = firm_contact[3]

            fund_info = basic_info.css('.fund-info .grey *::text').extract()
            if len(fund_info) != 0:
                company['asset_size'] = fund_info[0]
                company['fund_num'] = fund_info[1]
                company['manager_num'] = fund_info[3]
                company['establishment_date'] = fund_info[5]
                company['company_nature'] = fund_info[6]
        yield company

        scale_curve = response.css("#gmbdTags li::attr(data-value)").extract()

        for code in scale_curve:
            fund_scale = FundScale()
            fund_scale['_id'] = company['_id']
            url = self.get_url_by_company_and_code(company['_id'],code)
            data = requests.get(url).json()
            yield FundScale(company=company['_id'],fund_type=data['fundType'],x=data['x'],y=data['y'])

    def get_url_by_company_and_code(self, company, code):
        if not code:
            code = 0
        return "http://fund.eastmoney.com/Company/home/GetGmbdChart?gsid={}&fundType={}".format(company, code)
