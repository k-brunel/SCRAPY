import pymongo
from itemadapter import ItemAdapter
from scrapy import signals

class MongoPipeline:
    collection_name = "scrapy_citations"
    errors_collection_name = "scrapy_errors"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "DB_SCRAPY"),
        )
        crawler.signals.connect(pipeline.spider_error, signal=signals.spider_error)
        return pipeline

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]
        self.errors_collection = self.db[self.errors_collection_name]
        self.collection.create_index([("citation", pymongo.TEXT)], name='citation_index', unique=True)
        self.collection.create_index([("auteur", pymongo.ASCENDING)], name='auteur_index')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.collection.insert_one(ItemAdapter(item).asdict())
        except Exception as e:
            self.errors_collection.insert_one({'error': str(e), 'item': dict(item)})
            spider.logger.error(f"Error processing item: {e}")
        return item


    def spider_error(self, failure, response, spider):
        error_info = {
            'url': response.url,
            'exception': failure.getTraceback(),
        }
        self.errors_collection.insert_one(error_info)
        spider.logger.error(f"Error on {response.url}: {failure.getTraceback()}")

