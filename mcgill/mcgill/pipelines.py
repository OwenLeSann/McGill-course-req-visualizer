# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SQLitePipeline:
    collection_name = "mcgill_courses"
    
    def __init__(self, sqlite_db):
        self.sqlite_db = sqlite_db
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(sqlite_db = crawler.settings.get("SQLITE_DATABASE", "mcgill_courses.db"))
    
    def open_spider(self, spider):
        self.connection = sqlite3.connect(self.sqlite_db)
        self.c = self.connection.cursor()
        try:
            self.c.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.collection_name} (
                    title TEXT,
                    subject TEXT,
                    level TEXT,
                    course_code TEXT,
                    terms TEXT,
                    prerequisites TEXT,
                    prerequisite_urls TEXT,
                    corequisites TEXT,
                    corequisite_urls TEXT)
                ''')
            self.connection.commit()
        except sqlite3.OperationalError as e:
            spider.log(f"Error creating table: {e}")
       
    def close_spider(self, spider):
        self.connection.close()
     
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Concatenate lists into strings
        terms = ", ".join(adapter.get("terms")) if isinstance(adapter.get("terms"), list) else str(adapter.get("terms", ""))
        prerequisites = ", ".join(adapter.get("prerequisites")) if isinstance(adapter.get("prerequisites"), list) else str(adapter.get("prerequisites", ""))
        prerequisite_urls = ", ".join(adapter.get("prerequisite_urls")) if isinstance(adapter.get("prerequisite_urls"), list) else str(adapter.get("prerequisite_urls", ""))
        corequisites = ", ".join(adapter.get("corequisites")) if isinstance(adapter.get("corequisites"), list) else str(adapter.get("corequisites", ""))
        corequisite_urls = ", ".join(adapter.get("corequisite_urls")) if isinstance(adapter.get("corequisite_urls"), list) else str(adapter.get("corequisite_urls", ""))
        
        try:
            self.c.execute(f'''
                INSERT INTO {self.collection_name} (
                    title, subject, level, course_code, terms, prerequisites, prerequisite_urls, corequisites, corequisite_urls
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                adapter.get("title")[0],
                adapter.get("subject")[0],
                adapter.get("level")[0],
                adapter.get("course_code")[0],
                terms,
                prerequisites,
                prerequisite_urls,
                corequisites,
                corequisite_urls,
            ))
            self.connection.commit()
        except sqlite3.OperationalError as e:
            spider.log(f"Error inserting item into database: {e}")

        return item
