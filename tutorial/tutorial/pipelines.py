# -*- coding: utf-8 -*-
import pymysql
from .items import DingdianItem,ChapterItem
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
            file_url = "./noval/%s-%s.text"%(item['noval_name'],item['title'])
            with open(file_url,"w+") as f:
                f.write(item['p'].encode('utf-8'))
            self.cursor.execute("""SELECT id from noval WHERE title = %s""",(item['noval_name']))
            result = self.cursor.fetchone()
            print(result)
            # self.cursor.execute("""
            # INSERT INTO noval (noval_id, title, url)
            #                     VALUES (%s, %s, %s)
            # """,(
            #     item[]
            #     item['title'].encode('utf-8'),
            #     item['author'].encode('utf-8'),
            #     item['word_count'].encode('utf-8'),
            #     item['update_date'].encode('utf-8'),
            #     item['status'].encode('utf-8'),
            #     item['tag'].encode('utf-8')
            # ))
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()