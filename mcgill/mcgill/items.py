# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class McgillItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(serializer=str)
    subject = scrapy.Field(serializer=str)
    level = scrapy.Field(serializer=str)
    course_code = scrapy.Field(serializer=str)
    terms = scrapy.Field(serializer=str)
    prerequisites = scrapy.Field(serializer=str)
    prerequisite_urls = scrapy.Field(serializer=str)
    corequisites = scrapy.Field(serializer=str)
    corequisite_urls = scrapy.Field(serializer=str)
