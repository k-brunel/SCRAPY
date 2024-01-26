import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"

    def start_requests(self): #Crawler de page en page
        urls = [
            "https://quotes.toscrape.com/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        citations = response.xpath('//*[@class="quote"]')
        for citation in citations:
            myCitations = {
                "auteur": citation.xpath('.//*[@class="author"]/text()').get(),
                "citation": citation.xpath('.//*[@class="text"]/text()').get()
            }
            yield myCitations
        # go to the next page
        url = response.css(".next > a::attr(href)").get()
        if url is not None:
            yield response.follow(url=url, callback=self.parse)


# VERSION qui Modifie une citation pour vérifier le bon fonctionnement du pipeline (update le champs si similarité > 80%)
# import scrapy

# class JobsSpider(scrapy.Spider):
#     name = "jobs"

#     def start_requests(self):  # Crawler de page en page
#         urls = [
#             "https://quotes.toscrape.com/"
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         citations = response.xpath('//*[@class="quote"]')
#         for citation in citations:
#             myTest = citation.xpath('.//*[@class="text"]/text()').get()

#             # Ajoutez une condition pour vérifier si la citation correspond à celle spécifiée
#             if "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking." in myTest:
#                 self.logger.info(f"Original citation: {myTest}")
#                 myTest = "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking test !!!"
#                 self.logger.info(f"Modified citation: {myTest}")

#             myCitations = {
#                 "auteur": citation.xpath('.//*[@class="author"]/text()').get(),
#                 "citation": myTest
#             }
#             yield myCitations

#         # Passer à la page suivante
#         url = response.css(".next > a::attr(href)").get()
#         if url is not None:
#             yield response.follow(url=url, callback=self.parse)
