# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def open_spider(self,spider):
        self.conn = pymysql.connect(host="localhost",user="root",passwd="root",db="dingdian",charset="utf8")
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
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
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()