import scrapy

class JobsSpider(scrapy.Spider):
    name = "jobs"

    def start_requests(self):
        """
        Start Requests Function

        Sends initial requests to specified URLs.
        """
        urls = [
            "https://quotes.toscrape.com/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_error)

    def parse(self, response):
        """
        Parse Function

        Extracts quotes and authors from the page.
        """
        citations = response.xpath('//*[@class="quote"]')
        for citation in citations:
            yield {
                "auteur": citation.xpath('.//*[@class="author"]/text()').get(),
                "citation": citation.xpath('.//*[@class="text"]/text()').get(),
            }

        # Pagination
        next_page = response.css('li.next > a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def handle_error(self, failure):
        """
        Handle Error Function

        Handles request errors and generates logs on failure.
        """
        self.logger.error(f'Request failed: {failure.request.url}')
