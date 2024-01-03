# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

"""Pipeline used to store McgillItem fields into a normalized SQLite database."""
class SQLitePipeline:
    # Table names
    course_collection_name = "Courses"
    prerequisites_collection_name = "Prerequisites"
    corequisites_collection_name = "Corequisites"
    terms_collection_name = "Terms"
    course_terms_collection_name = "CourseTerms"
    
    """(self, cls) -> NoneType
    SQLitePipeline constructor method.
    """
    def __init__(self, sqlite_db):
        self.sqlite_db = sqlite_db
    
    """(cls, Crawler) -> cls
    Accesses the Crawler's settings and uses them to create a pipeline instance.
    """    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(sqlite_db = crawler.settings.get("SQLITE_DATABASE", "mcgill_courses.db"))
    
    """(self, Spider) -> NoneType
    When the spider is opened, initializes five collection tables in the SQLite database. 
    The spider logs any sqlite3 operational errors that may occur when initializing the tables.
    """
    def open_spider(self, spider):
        self.connection = sqlite3.connect(self.sqlite_db)
        self.c = self.connection.cursor()
        try:
            # Initializing tables
            self.c.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.course_collection_name} (
                    course_code TEXT PRIMARY KEY,
                    title TEXT,
                    subject TEXT,
                    level TEXT)
                ''')
            
            self.c.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.terms_collection_name} (
                    term TEXT PRIMARY KEY)
                ''')
            
            self.c.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.course_terms_collection_name} (
                    course_code TEXT,
                    term TEXT,
                    PRIMARY KEY (course_code, term),
                    FOREIGN KEY (course_code) REFERENCES {self.course_collection_name}(course_code),
                    FOREIGN KEY (term) REFERENCES {self.terms_collection_name}(term))
                ''')
            
            self.c.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.prerequisites_collection_name} (
                    course_code TEXT,
                    prerequisite TEXT,
                    prerequisite_url TEXT,
                    PRIMARY KEY (course_code, prerequisite),
                    FOREIGN KEY (course_code) REFERENCES {self.course_collection_name}(course_code),
                    FOREIGN KEY (prerequisite) REFERENCES {self.course_collection_name}(course_code))
                ''')
            
            self.c.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.corequisites_collection_name} (
                    course_code TEXT,
                    corequisite TEXT,
                    corequisite_url TEXT,
                    PRIMARY KEY (course_code, corequisite),
                    FOREIGN KEY (course_code) REFERENCES {self.course_collection_name}(course_code),
                    FOREIGN KEY (corequisite) REFERENCES {self.course_collection_name}(course_code))
                ''')
            
            self.connection.commit()
        except sqlite3.OperationalError as e:
            spider.log(f"Error creating table: {e}")
    
    """(self, Spider) -> NoneType
    Closes connection to the SQLite database once the spider is closed.
    """   
    def close_spider(self, spider):
        self.connection.close()

    """(self, Item, Spider) -> Item
    Loads the Item object's (McgillItem in this instance) fields into the database tables.
    The spider logs any sqlite3 Integrity and/or Operational errors that may occur during database
    transaction.
    """
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        try:
            # Inserting data into tables
            course_code = adapter.get("course_code")[0]

            self.c.execute(f'''
                INSERT OR IGNORE INTO {self.course_collection_name} (
                    course_code, title, subject, level
                ) VALUES (?, ?, ?, ?)
            ''', (
                course_code,
                adapter.get("title")[0],
                adapter.get("subject")[0],
                adapter.get("level")[0],
            ))

            terms = adapter.get("terms")
            
            terms_data = [(term,) for term in terms]
            self.c.executemany(f'''
                INSERT OR IGNORE INTO {self.terms_collection_name} (term) VALUES (?)
            ''', terms_data)

            course_terms_data = [(course_code, term) for term in terms]
            self.c.executemany(f'''
                INSERT OR IGNORE INTO {self.course_terms_collection_name} (course_code, term) VALUES (?, ?)
            ''', course_terms_data)

            # Checks if there are prerequisites/corequisites (and their respective urls) for a given course.
            # Only courses with prerequisites/corequisites are added to the prerequisites/corequisites tables.
            prerequisites = adapter.get("prerequisites")
            if prerequisites is not None:
                prerequisites_data = [
                    (course_code, prerequisite, prerequisite_url)
                    for prerequisite, prerequisite_url in zip(prerequisites, adapter.get("prerequisite_urls"))
                ]
                self.c.executemany(f'''
                    INSERT OR IGNORE INTO {self.prerequisites_collection_name} (
                        course_code, prerequisite, prerequisite_url
                    ) VALUES (?, ?, ?)
                ''', prerequisites_data)

            corequisites = adapter.get("corequisites")
            if corequisites is not None:
                corequisites_data = [
                    (course_code, corequisite, corequisite_url)
                    for corequisite, corequisite_url in zip(corequisites, adapter.get("corequisite_urls"))
                ]
                self.c.executemany(f'''
                    INSERT OR IGNORE INTO {self.corequisites_collection_name} (
                        course_code, corequisite, corequisite_url
                    ) VALUES (?, ?, ?)
                ''', corequisites_data)

            self.connection.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
            spider.log(f"Error inserting item into database: {e}")

        return item
