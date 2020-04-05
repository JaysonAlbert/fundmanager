from pymongo import MongoClient
import pandas as pd
import timeit

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
result = client['fundmanager']['assets'].aggregate([
    {
        '$match': {
            'published_date': {
                '$eq': '2019-12-31'
            }
        }
    }, {
        '$lookup': {
            'from': 'fund',
            'let': {
                'code': '$code'
            },
            'pipeline': [
                {
                    '$match': {
                        '$expr': {
                            '$eq': [
                                '$$code', '$code'
                            ]
                        }
                    }
                }, {
                    '$project': {
                        'company': 1,
                        'name': 1,
                        'type': 1,
                        '_id': 0
                    }
                }
            ],
            'as': 'fundInfo'
        }
    }, {
        '$replaceRoot': {
            'newRoot': {
                '$mergeObjects': [
                    '$$ROOT', {
                        '$arrayElemAt': [
                            '$fundInfo', 0
                        ]
                    }
                ]
            }
        }
    }, {
        '$match': {
            '$or': [
                {
                    'type': {
                        '$eq': '股票型'
                    }
                }, {
                    'type': {
                        '$eq': '混合型'
                    }
                }
            ]
        }
    }, {
        '$group': {
            '_id': '$company',
            'count': {
                '$sum': 1
            },
            'avg': {
                '$avg': '$head_shares'
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    }, {
        '$limit': 20
    }
])


def cc():
    print(pd.DataFrame(result))


cc()