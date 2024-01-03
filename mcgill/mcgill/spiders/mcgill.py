import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from mcgill.items import McgillItem

class McgillSpider(CrawlSpider):
    name = "mcgill"
    allowed_domains = ["www.mcgill.ca"]
    
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"

    rules = (Rule(LinkExtractor(restrict_xpaths="//h4[@class='field-content']/a"), callback="parse_item", follow=True, process_request="set_user_agent"), # Each course 
             Rule(LinkExtractor(restrict_xpaths="//li[@class='pager-next']/a"), process_request="set_user_agent") # Next page
             )

    # Changes user-agent displayed from Scrapy[version] to user_agent and sets initial domain
    def start_requests(self):
        yield scrapy.Request(url="https://www.mcgill.ca/study/2023-2024/courses/search", headers={
            "User-Agent": self.user_agent
        })
        
    # Sets user-agent to user_agent in each new link
    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        try:
            title = response.xpath("normalize-space(//h1[@id='page-title']/text())").get()
            if (title[1] == '"'): title = title[1:-1] # remove duplicate quotations
            title_parsed = title.split()
            subject = title_parsed[0]
            level = title_parsed[1][0] + "00"
            course_code = " ".join(title_parsed[:2])
            
            terms = response.xpath("normalize-space(//p[@class='catalog-terms']/text())").get()
            terms = terms[7:]
            
            prerequisites = response.xpath("//li/p[contains(text(), 'Prerequisite') or contains(text(), 'Pre-requisite')]/a/text()").extract()
            prerequisite_urls = response.xpath("//li/p[contains(text(), 'Prerequisite') or contains(text(), 'Pre-requisite')]/a/@href").extract()
            for i in range(len(prerequisite_urls)):
                prerequisite_urls[i] = response.urljoin(prerequisite_urls[i])
                
            corequisites = response.xpath("//li/p[contains(text(), 'Corequisite') or contains(text(), 'Co-requisite')]/a/text()").extract()
            corequisite_urls = response.xpath("//li/p[contains(text(), 'Corequisite') or contains(text(), 'Co-requisite')]/a/@href").extract()
            for i in range(len(corequisite_urls)):
                corequisite_urls[i] = response.urljoin(corequisite_urls[i])
            
            l = ItemLoader(item = McgillItem(), response = response)
            l.add_value("title", title)
            l.add_value("subject", subject)
            l.add_value("level", level)
            l.add_value("course_code", course_code)
            l.add_value("terms", terms)
            l.add_value("prerequisites", prerequisites)
            l.add_value("prerequisite_urls", prerequisite_urls)
            l.add_value("corequisites", corequisites)
            l.add_value("corequisite_urls", corequisite_urls)
            
            return l.load_item()
        except Exception as e:
            self.log(f"Error parsing item: {e} - URL: {response.url}")
        
    ''' without loading items container
    def parse_item(self, response):
        title = response.xpath("normalize-space(//h1[@id='page-title']/text())").get()
        if (title[1] == '"'): title = title[1:-1] # remove duplicate quotations
        title_parsed = title.split()
        subject = title_parsed[0]
        level = title_parsed[1][0] + "00"
        course_code = " ".join(title_parsed[:2])
        
        terms = response.xpath("normalize-space(//p[@class='catalog-terms']/text())").get()
        terms = terms[7:]
        
        prerequisites = response.xpath("//li/p[contains(text(), 'Prerequisite') or contains(text(), 'Pre-requisite')]/a/text()").extract()
        prerequisite_urls = response.xpath("//li/p[contains(text(), 'Prerequisite') or contains(text(), 'Pre-requisite')]/a/@href").extract()
        for i in range(len(prerequisite_urls)):
            prerequisite_urls[i] = response.urljoin(prerequisite_urls[i])
            
        corequisites = response.xpath("//li/p[contains(text(), 'Corequisite') or contains(text(), 'Co-requisite')]/a/text()").extract()
        corequisite_urls = response.xpath("//li/p[contains(text(), 'Corequisite') or contains(text(), 'Co-requisite')]/a/@href").extract()
        for i in range(len(corequisite_urls)):
            corequisite_urls[i] = response.urljoin(corequisite_urls[i])
        
        yield {
            # Format: 
            # {'title': 'AGEC 231 Economic Systems of Agriculture (3 credits)'}
            "title": title,
            "subject": subject,
            "level": level,
            "course_code": course_code,
            "terms": terms,
            "prerequisites": prerequisites,
            "prerequisite_urls": prerequisite_urls,
            "corequisites": corequisites,
            "corequisite_urls": corequisite_urls,
            "user-agent": response.request.headers["User-Agent"] # Works
        }
    '''
