import numpy
import requests


# 获取基金代码列表
def code_list():
    res = requests.get("http://fund.eastmoney.com/js/fundcode_search.js")
    codes = eval(res.content.decode('utf-8').split('=')[1][:-1])
    return numpy.array(codes)[:, 0]