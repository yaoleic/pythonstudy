# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
from scrapy.loader import ItemLoader
import re


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
   try:
       create_date = datetime.datetime.strptime(value,"%Y/%m/%d").date()
   except Exception as e:
       create_date = datetime.datetime.now().date()
   return create_date


def get_nums(value):
    nums = re.findall("\d", value)
    if nums:
        nums = nums[0]
    else:
        nums = 0
    return nums


def remove_comment(value):
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    praise_number = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    url = scrapy.Field()
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    url_object_id = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment),
        output_processor=Join(",")
    )