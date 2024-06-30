import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
django.setup()

from quotes.models import Quote, Author
from scrapy.crawler import CrawlerProcess
from scrapy import Spider

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author_name = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()

            author, created = Author.objects.get_or_create(fullname=author_name)
            Quote.objects.get_or_create(text=text, author=author, tags=tags)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

def run_spider():
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
    print("Quotes scraped successfully!")
