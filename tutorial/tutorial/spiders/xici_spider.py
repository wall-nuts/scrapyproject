#coding:utf-8
import scrapy,requests
from scrapy.cmdline import execute
from tutorial.items import XiciItem

class Xici(scrapy.Spider):
    name = 'xici'
    def start_requests(self):
        urls = [
            "http://www.xicidaili.com/nn/1/",
        ]
        headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Accept":"image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Referer":"http://www.xicidaili.com/nn/1",
        }
        for url in urls:
            yield scrapy.Request(url,headers=headers,callback=self.parse)

    def parse(self, response):
        table = response.xpath('//table[@id="ip_list"]')[0]
        trs = table.xpath('//tr')[1:]
        item = XiciItem()
        for tr in trs :
            pagetest = "http://www.baidu.com"
            ip = tr.xpath("td[2]/text()").extract()[0]
            port = tr.xpath("td[3]/text()").extract()[0]
            proxy = "http://"+ip+":"+port
            proxies={
                "http":proxy
            }
            try:
                response = requests.get(pagetest,timeout=1,proxies = proxies)
                print(response.status_code)
                if(response.status_code==200):
                    item['ip'] = ip
                    item['port'] = port
                    yield item
            except:
                print("connect failed!")
