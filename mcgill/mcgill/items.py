# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class McgillItem(scrapy.Item):
    title = scrapy.Field()
    subject = scrapy.Field()
    level = scrapy.Field()
    course_code = scrapy.Field()
    terms = scrapy.Field()
    prerequisites = scrapy.Field()
    prerequisite_urls = scrapy.Field()
    corequisites = scrapy.Field()
    corequisite_urls = scrapy.Field()
