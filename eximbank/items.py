import scrapy


class Article(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    link = scrapy.Field()
