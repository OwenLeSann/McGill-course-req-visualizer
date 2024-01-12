import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from mcgill.items import McgillItem


class McgillSpider(CrawlSpider):
    name = "mcgill"
    allowed_domains = ["www.mcgill.ca"]
    
    # My laptop's user agent, used to access websites that would normally block web-scraping bots
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"

    # For pageination
    rules = (Rule(LinkExtractor(restrict_xpaths="//h4[@class='field-content']/a"), callback="parse_item", follow=True, process_request="set_user_agent"), # Accesses each course page 
             Rule(LinkExtractor(restrict_xpaths="//li[@class='pager-next']/a"), process_request="set_user_agent") # Accesses the next page
             )

    """(self) -> NoneType
    Changes Scrapy[version] to user_agent defined above and sets Crawler's initial domain to the McGill eCalendar courses page (url).
    """
    def start_requests(self):
        yield scrapy.Request(url="https://www.mcgill.ca/study/2023-2024/courses/search", headers={
            "User-Agent": self.user_agent
        })
        
    """(self, Request, Spider) -> Request
    Setter method. Sets user-agent to that listed above, used in pageination to ensure bot's user-agent is never disclosed.
    """
    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    """(self, Response) -> McgillItem
    Scrapes data from webpage using XPath expressions. Data is then parsed and stored in the fields
    of the McgillItem class in the items.py file. Any exception that is raised is logged by the Crawler.
    """
    def parse_item(self, response):
        try:
            # Parsing data from XPath
            title = response.xpath("normalize-space(//h1[@id='page-title']/text())").get()
            if (title[1] == '"'): title = title[1:-1] # Remove duplicate quotations (webpage formatting error)
            title_parsed = title.split()
            subject = title_parsed[0]
            level = title_parsed[1][0] + "00"
            course_code = " ".join(title_parsed[:2])
            
            terms = response.xpath("normalize-space(//p[@class='catalog-terms']/text())").get()
            terms = terms[7:].split(", ")
            
            prerequisites = response.xpath("//li/p[contains(text(), 'Prerequisite') or contains(text(), 'Pre-requisite')]/a/text()").extract()
            prerequisite_urls = response.xpath("//li/p[contains(text(), 'Prerequisite') or contains(text(), 'Pre-requisite')]/a/@href").extract()
            for i in range(len(prerequisite_urls)):
                prerequisite_urls[i] = response.urljoin(prerequisite_urls[i])
                
            corequisites = response.xpath("//li/p[contains(text(), 'Corequisite') or contains(text(), 'Co-requisite')]/a/text()").extract()
            corequisite_urls = response.xpath("//li/p[contains(text(), 'Corequisite') or contains(text(), 'Co-requisite')]/a/@href").extract()
            for i in range(len(corequisite_urls)):
                corequisite_urls[i] = response.urljoin(corequisite_urls[i])
            
            # Use item loader to load McgillItem fields with parsed data
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
        