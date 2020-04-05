import tushare as ts

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('localhost', 27017)
db = client['fundmanager']

pro = ts.pro_api('9a05017c09bfa11f48d8924726e2e77d43e4ecf481f2f616fee5c512')
for d in pro.stock_basic(list_status='L', fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs').to_dict('record'):
    d['_id'] = d['ts_code']
    try:
        db['stock_basic'].insert_one(d)
    except DuplicateKeyError as e:
        pass
