import pymongo

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['fundmanager']

agr = [
    {
        '$project': {
            'funds': True,
            'published_date': True,
            '_id': False
        }
    }, {
        '$unwind': {
            'path': '$funds'
        }
    }, {
        '$project': {
            'code': {
                '$arrayElemAt': [
                    '$funds', 0
                ]
            },
            'value': {
                '$arrayElemAt': [
                    '$funds', 4
                ]
            }
        }
    }
]


def process(record):
    for i in record.funds:
        yield i


records = (record['funds'] for record in  db.assets.find({'published_date': "2019-12-31"}) if record['published_date'] == '2019-12-31')

lines = ([line for line in pack if ',' in line[4]] for pack in records)

print(next(lines))