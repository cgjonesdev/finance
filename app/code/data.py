from pprint import pprint

from pymongo import MongoClient
from bson import ObjectId


class DataConnector(object):

    def __init__(self, collection_name):
        client = MongoClient()
        db = client['finance']
        self.collection = db[collection_name]

    def __iter__(self):
        return (item for item in self.collection.find())

    def __getitem__(self, _id):
        return self.collection.find_one({'_id': ObjectId(_id)})

    def __add__(self, data):
        _id = self.collection.insert(data)
        return list(self.collection.find(data))[0]

    def __sub__(self, _id):
        self.collection.remove({'_id': ObjectId(_id)})

    def __iadd__(self, udpate_info):
        _id, data = udpate_info
        self.collection.replace_one({'_id': ObjectId(_id)}, data)

    def clear(self):
        for document in self:
            self - document[_id]
        return list(self)

    def get_by_name(self, name):
        for item in self:
            if name in item.values():
                return item


if __name__ == '__main__':
    dc = DataConnector('balance_sheet')
    pprint(list(dc))
    dc.clear()
