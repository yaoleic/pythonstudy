# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import pymysql
from twisted.enterprise import adbapi
import pymysql.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleExpoter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    """
    mysql 同步写入数据库
    """

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='article_spider',charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
        insert into articles(title,create_time,praise_number,fav_nums,url,comment_nums,front_image_url,front_image_path,url_object_id,tags,content) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item["title"],item["create_time"],item["praise_number"],item["fav_nums"],item["url"],item["comment_nums"],item["front_image_url"],item["front_image_path"],item["url_object_id"],item["tags"],item["content"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    """
    mysql 异步写入数据库
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def do_insert(self,cursor,item):
        insert_sql = """
                insert into articles(title,create_time,praise_number,fav_nums,url,comment_nums,front_image_url,front_image_path,url_object_id,tags,content) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (
        item["title"], item["create_time"], item["praise_number"], item["fav_nums"], item["url"], item["comment_nums"],
        item["front_image_url"], item["front_image_path"], item["url_object_id"], item["tags"], item["content"]))

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self,failure,item,spider):
        print(failure)


    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings["MYSQL_HOST"],
            user = settings["MYSQL_USER"],
            db = settings["MYSQL_DBNAME"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("pymysql",**dbparams)
        return cls(dbpool)


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok,value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item


