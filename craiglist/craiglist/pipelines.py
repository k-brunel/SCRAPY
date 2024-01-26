# # # Define your item pipelines here
# # #
# # # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # # useful for handling different item types with a single interface
# # import pymongo
# # from itemadapter import ItemAdapter


# # class MongoPipeline:
# #     collection_name = "scrapy_citations"

# #     def __init__(self, mongo_uri, mongo_db):
# #         self.mongo_uri = mongo_uri
# #         self.mongo_db = mongo_db

# #     @classmethod
# #     def from_crawler(cls, crawler):
# #         return cls(
# #             mongo_uri=crawler.settings.get("MONGO_URI"),
# #             mongo_db=crawler.settings.get("MONGO_DATABASE", "DB_SRAPY"),
# #         )

# #     def open_spider(self, spider):
# #         self.client = pymongo.MongoClient(self.mongo_uri)
# #         self.db = self.client[self.mongo_db]

# #     def close_spider(self, spider):
# #         self.client.close()

# #     def process_item(self, item, spider):
# #         self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
# #         return item


# # # Define your item pipelines here
# # #
# # # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # # useful for handling different item types with a single interface
# import pymongo
# from itemadapter import ItemAdapter
# from pymongo.errors import DuplicateKeyError

# class MongoPipeline:
#     collection_name = "scrapy_citations"

#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get("MONGO_URI"),
#             mongo_db=crawler.settings.get("MONGO_DATABASE", "DB_SRAPY"),
#         )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#         self.collection = self.db[self.collection_name]
#         self.collection.create_index("citation", unique=True)  # Crée un index unique sur le champ de la citation

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         try:
#             self.collection.insert_one(ItemAdapter(item).asdict())
#         except DuplicateKeyError:
#             spider.logger.warning(f"Duplicate item found: {item!r}")

#         return item

#a garder
# import pymongo
# from itemadapter import ItemAdapter
# from pymongo.errors import DuplicateKeyError
# from fuzzywuzzy import fuzz

# class MongoPipeline:
#     collection_name = "scrapy_citations"

#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get("MONGO_URI"),
#             mongo_db=crawler.settings.get("MONGO_DATABASE", "DB_SRAPY"),
#         )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#         self.collection = self.db[self.collection_name]
#         self.collection.create_index("citation", unique=True)
#         self.collection.create_index("auteur")  # Crée un index sur le champ "auteur"

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         citation = item['citation']
#         auteur = item['auteur']

#         # La citation n'est pas trouvée dans la base parmi les citations de cet auteur
#         if not self.collection.find_one({'auteur': auteur, 'citation': citation}):
#             # Recherche de citations similaires de cet auteur dans la base de données
#             similar_citations = self.collection.find({
#                 'auteur': auteur,
#                 'citation': {'$regex': citation, '$options': 'i'}
#             })

#             for similar_citation in similar_citations:
#                 similarity_score = fuzz.ratio(citation, similar_citation['citation'])
#                 # Si des citations similaires sont trouvées mise à jour (seuil de similarité de 80%)
#                 if similarity_score > 80:  
#                     spider.logger.info(f"Updating similar item: {similar_citation['citation']} with {citation}")
#                     try:
#                         self.collection.update_one({'_id': similar_citation['_id']}, {'$set': ItemAdapter(item).asdict()})
#                         return item  # Retourne après la mise à jour, évitant l'insertion
#                     except DuplicateKeyError:
#                         spider.logger.warning(f"Duplicate item found during update: {item!r}")

#             # Cas 3: La citation n'existe pas dans la base, l'insérer
#             try:
#                 self.collection.insert_one(ItemAdapter(item).asdict())
#             except DuplicateKeyError:
#                 spider.logger.warning(f"Duplicate item found during insert: {item!r}")

#         return item



import pymongo
from itemadapter import ItemAdapter
from pymongo.errors import DuplicateKeyError
from difflib import SequenceMatcher

class MongoPipeline:
    collection_name = "scrapy_citations"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "DB_SRAPY"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]
        self.collection.create_index("citation", unique=True)
        self.collection.create_index("auteur")  # Crée un index sur le champ "auteur"

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        citation = item['citation']
        auteur = item['auteur']

        # La citation n'est pas trouvée dans la base parmi les citations de cet auteur
        if not self.collection.find_one({'auteur': auteur, 'citation': citation}):
            # Recherche de citations similaires de cet auteur dans la base de données
            similar_citations = self.collection.find({
                'auteur': auteur,
            })

            for similar_citation in similar_citations:
                similarity_score = SequenceMatcher(None, citation, similar_citation['citation']).ratio()
                # Si des citations similaires sont trouvées mise à jour (seuil de similarité de 80%)
                if similarity_score > 0.8:  
                    spider.logger.info(f"Updating similar item: {similar_citation['citation']} with {citation}")
                    try:
                        self.collection.update_one({'_id': similar_citation['_id']}, {'$set': ItemAdapter(item).asdict()})
                        return item  # Retourne après la mise à jour, évitant l'insertion
                    except DuplicateKeyError:
                        spider.logger.warning(f"Duplicate item found during update: {item!r}")

            # Cas 3: La citation n'existe pas dans la base, l'insérer
            try:
                self.collection.insert_one(ItemAdapter(item).asdict())
            except DuplicateKeyError:
                spider.logger.warning(f"Duplicate item found during insert: {item!r}")

        return item
