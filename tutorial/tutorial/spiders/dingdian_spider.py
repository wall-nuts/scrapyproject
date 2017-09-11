import re
import scrapy
# from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import Request
from ..items import DingdianItem

class Dingdian(scrapy.Spider):

    name = 'dingdian'
    allowed_domains = ['x23us.com']
    base_url = 'http://www.x23us.com/class/'
    baseurl = '.html'
    def start_requests(self):
        for i in range(1,11):
            url = self.base_url + str(i) + '_1' + self.baseurl
            yield Request(url,self.parse)
        yield Request('http://www.x23us.com/quanben/1',callback = self.parse)

    def parse(self, response):
        max_num = response.selector.xpath('//a[@class="last"]/text()').extract()
        baseurl = response.url[:-7]
        for num in range(1,int(max_num[0]) + 1):
            url = baseurl + '_' + str(num) + self.baseurl
            yield Request(url,callback=self.get_name)

    def get_name(self,response):
        tds = response.selector.xpath('//*[@id="content"]/dd[1]/table/tbody/tr[2]/td[1]/a[2]')
        print(tds)