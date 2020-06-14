from rediscluster import RedisCluster
from fundmanager.spiders.utils import code_list

rc = RedisCluster('127.0.0.1', '6379')


def feed_manager_url():
    for code in code_list():
        url = "http://fundf10.eastmoney.com/jjjl_{}.html".format(code)
        rc.sadd('manager:start_urls',url)


def feed_fund_details_url():
    start_year = "2019"  # 起始年份
    url_format = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year={}"

    for code in code_list():
        url = url_format.format(code, start_year)
        rc.sadd('fund-details:start_urls', url)


def feed_company_url():
    rc.sadd('company:start_urls','http://fund.eastmoney.com/company/default.html')


if __name__ == '__main__':
    feed_manager_url()
    feed_fund_details_url()
    feed_company_url()