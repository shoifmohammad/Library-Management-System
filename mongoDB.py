import pymongo

client = pymongo.MongoClient("mongodb://test:13572468@library-management-syst-shard-00-00.20env.mongodb.net:27017,library-management-syst-shard-00-01.20env.mongodb.net:27017,library-management-syst-shard-00-02.20env.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-jt2zdr-shard-0&authSource=admin&retryWrites=true&w=majority")

db = client.get_database('library')