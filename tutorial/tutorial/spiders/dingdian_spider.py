#coding:utf-8
import re
import scrapy,pymysql
# from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import Request
from ..items import DingdianItem,ChapterItem

class Dingdian(scrapy.Spider):

    name = 'dingdian'
    allowed_domains = ['x23us.com']
    base_url = 'http://www.x23us.com/class/'
    baseurl = '.html'
    def start_requests(self):
        for i in range(1,2):
            url = self.base_url + str(i) + '_1' + self.baseurl
            yield Request(url,self.parse,meta={'num':i})
        # yield Request('http://www.x23us.com/quanben/1',callback = self.parse,meta={'num':10})

    def parse(self, response):
        max_num = response.selector.xpath('//a[@class="last"]/text()').extract()
        baseurl = response.url[:-7]
        for num in range(1,int(max_num[0]) + 1):
            url = baseurl + '_' + str(num) + self.baseurl
            yield Request(url,callback=self.get_name,meta={'num':response.meta['num']})

    def get_name(self,response):
        tags = ['玄幻魔法','武侠修真','都市言情','历史军事','侦探推理','网游动漫','科幻小说','恐怖灵异','散文诗词','其他','全本']
        item = DingdianItem()
        for i in range(len(response.selector.xpath('//td[@class="L"]/a[2]/text()').extract())):
            item['title'] = response.selector.xpath('//td[@class="L"]/a[2]/text()').extract()[i]
            item['author'] = response.selector.xpath('//tr[@bgcolor="#FFFFFF"]/td[3]/text()').extract()[i]
            item['word_count'] = response.selector.xpath('//tr[@bgcolor="#FFFFFF"]/td[4]/text()').extract()[i]
            item['update_date'] = response.selector.xpath('//tr[@bgcolor="#FFFFFF"]/td[5]/text()').extract()[i]
            item['status'] = response.selector.xpath('//tr[@bgcolor="#FFFFFF"]/td[6]/text()').extract()[i]
            item['tag'] = tags[response.meta['num']-1]
            yield item
            paper_url = response.selector.xpath('//td[@class="L"]/a[2]/@href').extract()[i]
            yield Request(paper_url,callback=self.get_chapter,meta={'noval_name':item['title']})

    def get_chapter(self,response):
        base_url = response.url
        chapter_urls = response.selector.xpath('//td[@class="L"]/a/@href').extract()
        for i in range(len(chapter_urls)):
            url = base_url + chapter_urls[i]
            title = response.selector.xpath('//td[@class="L"]/a/text()').extract()[i]
            yield Request(url,callback=self.get_paper,meta={'noval_name':response.meta['noval_name'],'title':title})

    def get_paper(self,response):
        item = ChapterItem()
        item['noval_name'] = response.meta['noval_name']
        item['title'] = response.meta['title']
        item['p']= response.selector.xpath('//dd[@id="contents"]/text()').extract()
        yield item