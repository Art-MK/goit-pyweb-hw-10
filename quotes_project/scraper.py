import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
django.setup()

import scrapy
from scrapy.crawler import CrawlerProcess
from quotes.models import Quote, Author

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author_name = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()

            author, created = Author.objects.get_or_create(fullname=author_name)
            Quote.objects.create(text=text, author=author, tags=tags)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

def run_spiders():
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()

if __name__ == "__main__":
    run_spiders()
