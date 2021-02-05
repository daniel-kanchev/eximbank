import scrapy
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from eximbank.items import Article


class EximSpider(scrapy.Spider):
    name = 'exim'
    allowed_domains = ['eximbank.gov.tr']
    start_urls = ['https://www.eximbank.gov.tr/tr/duyurular']

    def parse(self, response):
        years = response.xpath('//div[@class="category-item"]')
        for y in years:
            link = y.xpath('./a/@href').get()
            year = y.xpath('./a//text()').get().split()[0]
            yield response.follow(link, self.parse_year, cb_kwargs=dict(year=year))

    def parse_year(self, response, year):
        links = response.xpath('//a[@class="details-link"]/@href').getall()
        yield from response.follow_all(links, self.parse_article, cb_kwargs=dict(year=year))

    def parse_article(self, response, year):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2//text()').get()
        link = response.urljoin(response.xpath('//li[@class="pdf"]/a/@href').get())

        item.add_value('title', title)
        item.add_value('year', year)
        item.add_value('link', link)

        return item.load_item()
