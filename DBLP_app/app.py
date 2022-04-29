import json
from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from bson.son import SON

APP_PATH = "DBLP_app"
HOST = "localhost"
USER = "root"
PASSWD = "pass12345"
PORT = 27017

#TODO: Rédiger DOCSTRINGS
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
    def import_json(cls, fname):
        datas = []
        f = open(fname, 'r')
        with open(fname, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                except:
                    continue
                datas.append(data)
        try :
            cls.collection.insert_many(datas)
        except BulkWriteError as bwe:
            print("Writing Error Details " ,bwe.details)
            pass


    @classmethod
    def count(cls):
        document_count = cls.collection.count_documents({})

        count_command = SON([("count", cls.collection.name)])
        explain = cls.db.command("explain", count_command, verbosity='executionStats')
        print("Temps d'éxecution (ms) : " + str(explain["executionStats"]["executionTimeMillis"]))
        
        return document_count


    @classmethod
    def get_documents(cls, **kwargs):
        documents = []
        request = {}

        for key in kwargs:
            request[key] = kwargs[key]

        cursor = cls.collection.find(request)
        
        find_command = SON([("find", cls.collection.name), ("filter", request)])

        explain = cls.db.command("explain", find_command, verbosity='executionStats')
        print("Temps d'éxecution (ms) : " + str(explain["executionStats"]["executionTimeMillis"]))

        for document in cursor:
            documents.append(document)

        return documents
   

    @classmethod
    def get_informations(cls, pipeline):

        aggregat = cls.collection.aggregate(pipeline)
        aggregat_command = SON([("aggregate", cls.collection.name), ("pipeline", pipeline), ("cursor", {})])
        explain = cls.db.command("explain", aggregat_command, verbosity='executionStats')
        try:
            print("Temps d'éxecution (ms) : " + str(explain["executionStats"]["executionTimeMillis"]))
        except:
            print("Temps d'éxecution (ms) : " + str(explain["stages"][0]["$cursor"]["executionStats"]["executionTimeMillis"]))

        return list(aggregat)


    #TODO: Intégrer l'affichage du temps d'éxecution
    @classmethod
    def get_distinct_entries(cls, *args, **kwargs):
        documents = []
        request = {}
        filter = {}

        for key in kwargs:
            request[key] = kwargs[key]

        for key in args:
            filter[key] = 1

        cursor = cls.collection.find(request, filter).distinct(args[0])

        for document in cursor:
            documents.append(document)

        return documents

    #TODO: Intégrer l'affichage du temps d'éxecution
    @classmethod
    def get_documents_ordered(cls, *args, **kwargs):
        documents = []
        request = {}
        filter = {}

        for key in kwargs:
            request[key] = kwargs[key]

        for key in args:
            filter[key] = 1

        cursor = cls.collection.find(request, filter).sort(args[0])

        for document in cursor:
            documents.append(document)

        return documents


    #TODO: Réécrire la fonction 'count_documents' malencontreusement supprimée
        

if __name__ == "__main__":

    # Connexion
    print("Connexion à la BDD.")
    MongoConnector.connexion("DBLP", "publis")
    print("BDD connectée !")

    # Importation
    # print("Importation des données.")
    # MongoConnector.import_json(f"{APP_PATH}/data/dblp.json")
    # print("Données importées !")

    print("------------------------------------------------------------")

    # Comptage
    print("Comptage du nombre de documents.")
    print("Fonction 'count_documents' :")
    document_count = MongoConnector.count()
    print("------------------------------")
    print("Aggregation de commande :")
    pipeline_count = [{"$count":"count"}]
    document_count = MongoConnector.get_informations(pipeline_count)

    print("------------------------------------------------------------")

    # Récupération des documents de type "Book"
    print("Récupération des documents de type 'Book' :")
    print("Fonction 'find' :")
    books = MongoConnector.get_documents(
        type="Book"
    )
    print("------------------------------")
    print("Aggregation de commande :")
    pipeline_books = [{"$match":{"type":"Book"}}]
    books = MongoConnector.get_informations(pipeline_books)

    print("------------------------------------------------------------")

    # Récupération des documents de type "Book" sortis après 2014
    print("Récupération des documents de type 'Book' parus après 2014:")
    print("Fonction 'find' :")
    books_after_2014 = MongoConnector.get_documents(
        type="Book",
        year={"$gt":2014}
    )
    print("------------------------------")
    print("Aggregation de commande :")
    pipeline_books_after_2014 = [{"$match":{"type":"Book", "year":{"$gt":2014}}}]
    books_after_2014 = MongoConnector.get_informations(pipeline_books_after_2014)

    print("------------------------------------------------------------")
    
    # Récupération des publications de l'auteur "Toru Ishida"
    print("Récupération des publication des l'auteur 'Toru Ishida' :")
    print("Fonction 'find' :")
    publications_toru_ishida = MongoConnector.get_documents(
        authors="Toru Ishida"
    )
    print("------------------------------")
    print("Aggregation de commande :")
    pipeline_publications_toru_ishida = [{"$match":{"authors":"Toru Ishida"}}]
    publications_toru_ishida = MongoConnector.get_informations(pipeline_publications_toru_ishida)
    
    print("------------------------------------------------------------")

    # Lister tous les auteurs distincts
    print("Récupération de la liste des auteurs distincts :")
    print("Fonction 'find' :")
    liste_auteurs = MongoConnector.get_distinct_entries(
        "authors"
    )
    print("------------------------------")
    print("Aggregation de commande :")
    pipeline_distinct_authors = [
        {"$unwind":"$authors"},
        {"$group":{"_id":"$authors"}}
    ]
    liste_auteurs = MongoConnector.get_informations(pipeline_distinct_authors)
    
    print("------------------------------------------------------------")

    #Trier les publications de "Toru Ishida" par titre de livre
    print("Tri des publication des 'Toru Ishida' par titre de livre :")
    print("Fonction 'find' :")
    publications_toru_ishida_ordered = MongoConnector.get_documents_ordered(
        "title",
        authors="Toru Ishida"
    )
    print("------------------------------")
    print("Aggregation de commande :")
    pipeline_publications_tou_ishida_by_title = [
        {"$match":{"authors":"Toru Ishida"}},
        {"$sort":SON([("title", 1)])}
    ]
    publications_toru_ishida_ordered = MongoConnector.get_informations(pipeline_publications_tou_ishida_by_title)

    print("------------------------------------------------------------")

    # Compter le nombre de ses publications
    print("Comptage du nombre de ses publications :")
    # print("Fonction 'find' :")
    # nombre_publications_toru_ishida = MongoConnector.count_documents(publications_toru_ishida)
    # print("------------------------------")
    print("Aggregation de commande :")
    pipeline_publications_tou_ishida = [
        {"$match":{"authors":"Toru Ishida"}},
        {"$count":"title"}
    ]
    nombre_publications_toru_ishida = MongoConnector.get_informations(pipeline_publications_tou_ishida)

    print("------------------------------------------------------------")

    # Compter le nombre de publications depuis 2011 et par type.
    print("Comptage du nombre de publications depuis 2011 et par type :")
    print("Aggregation de commande :")
    pipeline_after_2011_by_type = [
            {"$match":{"year": {"$gte": 2011}}},
            {"$group":{"_id":"$type","count":{"$sum":1}}},
            {"$sort":SON([("count", 1)])}
        ]
    nombre_publications_after_2011_by_type = MongoConnector.get_informations(pipeline_after_2011_by_type)

    print("------------------------------------------------------------")

    # Compter le nombre de publications par auteur et trier le résultat par ordre croissant.
    print("Comptage du nombre de publications par auteur et trier le résultat par ordre croissant :")
    print("Aggregation de commande :")
    pipeline_by_ordered_author = [
        {"$unwind":"$authors"},
        {"$group":{"_id":"$authors","count":{"$sum":1}}},
        {"$sort":SON([("count", 1)])}
    ]
    publication_by_ordered_author_number = MongoConnector.get_informations(pipeline_by_ordered_author)
    
    print("------------------------------------------------------------")

    # Deconnexion
    print("Déconnexion de la BBD.")
    MongoConnector.deconnexion()
    print("BDD déconnectée !")