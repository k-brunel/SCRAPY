# Import necessary libraries
import pymongo
from itemadapter import ItemAdapter
from scrapy import signals

class MongoPipeline:
    # Define MongoDB collection names
    collection_name = "scrapy_citations"
    errors_collection_name = "scrapy_errors"

    def __init__(self, mongo_uri, mongo_db):
        """
        Initialize the MongoDB pipeline.

        Args:
            mongo_uri (str): The MongoDB URI.
            mongo_db (str): The MongoDB database name.
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        Create an instance of the pipeline using Scrapy settings.

        Args:
            crawler: The Scrapy crawler instance.

        Returns:
            MongoPipeline: An instance of the pipeline.
        """
        # Create an instance of the pipeline with MongoDB configuration from Scrapy settings
        pipeline = cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "DB_SCRAPY"),
        )
        # Connect the pipeline to Scrapy's spider_error signal
        crawler.signals.connect(pipeline.spider_error, signal=signals.spider_error)
        return pipeline

    def open_spider(self, spider):
        """
        Open the MongoDB connection and set up collections and indexes.

        Args:
            spider: The Scrapy spider.
        """
        # Establish a connection to MongoDB
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # Create or retrieve collections
        self.collection = self.db[self.collection_name]
        self.errors_collection = self.db[self.errors_collection_name]
        # Create indexes for efficient querying
        self.collection.create_index([("citation", pymongo.TEXT)], name='citation_index', unique=True)
        self.collection.create_index([("auteur", pymongo.ASCENDING)], name='auteur_index')

    def close_spider(self, spider):
        """
        Close the MongoDB connection when the spider is closed.

        Args:
            spider: The Scrapy spider.
        """
        # Close the MongoDB client connection
        self.client.close()

    def process_item(self, item, spider):
        """
        Process a scraped item and insert it into the MongoDB collection.

        Args:
            item: The scraped item.
            spider: The Scrapy spider.

        Returns:
            item: The processed item.
        """
        try:
            # Insert the item into the MongoDB collection after adapting it
            self.collection.insert_one(ItemAdapter(item).asdict())
        except Exception as e:
            # Handle exceptions by storing error information and logging
            self.errors_collection.insert_one({'error': str(e), 'item': dict(item)})
            spider.logger.error(f"Error processing item: {e}")
        return item

    def spider_error(self, failure, response, spider):
        """
        Handle spider errors by recording URL and exception information.

        Args:
            failure: The exception failure.
            response: The response causing the error.
            spider: The Scrapy spider.
        """
        error_info = {
            'url': response.url,
            'exception': failure.getTraceback(),
        }
        # Store error information in the errors collection and log the error
        self.errors_collection.insert_one(error_info)
        spider.logger.error(f"Error on {response.url}: {failure.getTraceback()}")
