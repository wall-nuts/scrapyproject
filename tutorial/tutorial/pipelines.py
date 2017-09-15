# -*- coding: utf-8 -*-
import pymysql,os,PIL
from .items import DingdianItem,ChapterItem,XiciItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def open_spider(self,spider):
        self.conn = pymysql.connect(host="localhost",user="root",passwd="root",db="dingdian",charset="utf8")
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        if(isinstance(item,DingdianItem)):
            self.cursor.execute("""
            INSERT INTO noval (title, author, word_count, update_date, status, tag)  
                                VALUES (%s, %s, %s, %s, %s, %s)
            """,(
                item['title'].encode('utf-8'),
                item['author'].encode('utf-8'),
                item['word_count'].encode('utf-8'),
                item['update_date'].encode('utf-8'),
                item['status'].encode('utf-8'),
                item['tag'].encode('utf-8')
            ))
            self.conn.commit()
            return item
        elif(isinstance(item,ChapterItem)):
            novalurl = './noval/%s'%item['noval_name']
            if not os.path.exists(novalurl):
                os.mkdir(novalurl)
            file_url = u"D:/sss/scrapyproject/tutorial/noval/%s/%s.txt"%(item['noval_name'],item['title'])
            with open(file_url,"ab+") as f:
                for i in item['p']:
                    j = i+'\r\n'
                    f.write(j.encode('utf-8'))
            self.cursor.execute("""SELECT id from noval WHERE title = %s""",(item['noval_name']))
            result = self.cursor.fetchone()
            print(item['title'],file_url.encode('utf-8'))
            sql = """
                INSERT INTO chapter(noval_id,title,url) VALUES (%d,%s,%s)
            """%(result[0],item['title'].encode('utf-8'),file_url.encode('utf-8'))
            self.cursor.execute(sql)
            self.conn.commit()
            return item
        elif(isinstance(item,XiciItem)):
            self.cursor.execute("""
            INSERT INTO ip_pool (ip, port)
                                VALUES (%s, %s)
            """,(
                item['ip'].encode('utf-8'),
                item['port'].encode('utf-8'),
            ))
            self.conn.commit()
            return item
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()

