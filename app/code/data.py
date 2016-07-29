from pprint import pprint

from pymongo import MongoClient


class DataConnector(object):

    def __init__(self, db_name, collection_name):
        client = MongoClient()
        db = client[db_name]
        self.collection = db[collection_name]

    def __iter__(self):
        return (item for item in self.collection.find())

    def __getitem__(self, data):
        return self.collection.find(data)

    def __add__(self, data):
        _id = self.collection.insert(data)
        return list(self.collection.find(data))[0]

    def __sub__(self, data):
        self.collection.remove(data)

    def __iadd__(self, data):
        self.collection.update(data)

    def clear(self):
        for document in self:
            self - document
        return list(self)


if __name__ == '__main__':
    dc = DataConnector('finance', 'balance_sheet')
