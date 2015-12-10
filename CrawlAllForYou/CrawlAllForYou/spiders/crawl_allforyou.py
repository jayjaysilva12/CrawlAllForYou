from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from ..items import CrawlallforyouItem
from time import gmtime, strftime
import scrapy
import re

class CrawlAllforyouSpider(CrawlSpider):
    ctr=0
    name = 'crawlallforyou'
    allowed_domains = ['allforyou.sg']
    start_urls = ['http://www.allforyou.com.sg/']
    rules = [Rule(LinkExtractor(allow=r'.+/\S+-\w+',deny=(r'.+.filter.+',r'.+.user.+',r'.+.aspx.+',r'.+signin.+','.+blog.+')),callback='parse_items',follow=True)]
    
    item = CrawlallforyouItem()
    
    def parse_items(self, response):
		for sel in response.xpath("//div[contains(@class, 'prod-data')]"):
			item = CrawlallforyouItem()
			self.ctr+=1
			print response
			item['crawl_time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
			item['urls'] = response.url	
			item['image'] = sel.xpath("@data-imgurl").extract()		
			item['out_of_stock'] = sel.xpath("@data-outofstock").extract()
			item['title'] = sel.xpath("@data-name").extract()
			item['offer'] = sel.xpath("@data-hasoffers").extract()	
			item['retailer_sku_code'] = sel.xpath("@id").extract()
			item['sku'] = sel.xpath("@data-newprodid").extract()
			item['desc'] = sel.xpath("@data-desc").extract()
			item['price'] = sel.xpath("@data-price").extract()
			print self.ctr
			#item['categories'] = cat[x:]
			yield item