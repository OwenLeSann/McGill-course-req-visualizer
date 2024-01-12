# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


"""Class used to neatly store scraped data from the McgillSpider Crawler into fields.

Fields
str title
str subject
str level
str course_code
list[str] terms
list[str] prerequisites
list[str] prerequisite_urls
list[str] corequisites
list[str] corequisite_urls
"""
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
