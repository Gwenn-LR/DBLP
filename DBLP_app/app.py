import json

from pymongo import MongoClient

APP_PATH = "DBLP_app"
HOST = "localhost"
USER = "root"
PASSWD = "pass12345"
PORT = 27017

class MongoConnector:

    @classmethod
    def connexion(cls, *args):
        cls.client = MongoClient(
            host = HOST,
            username = USER,
            password = PASSWD,
            port = PORT
        )

        if args:
            cls.db = cls.client[args[0]]
            cls.collection = cls.db[args[1]]


    @classmethod
    def deconnexion(cls):
        cls.client.close()


    @classmethod
    def select_database(cls, db):
        cls.db = cls.client[db]


    @classmethod
    def select_collection(cls, collection):
        cls.collection = cls.db[collection]


    @classmethod
    def import_json(cls, fname):
        datas = []
        f = open(fname, 'r')
        with open(fname, 'r') as f:
            for line in f:
                line = line.replace('^', "**")
                try:
                    data = json.loads(line)
                except:
                    continue
                datas.append(data)
        cls.collection.insert_many(datas)

if __name__ == "__main__":

    MongoConnector.connexion("DBLP", "publis")
    MongoConnector.import_json(f"{APP_PATH}/data/dblp.json")
    MongoConnector.deconnexion()
    print("OK")