# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobboleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """

        :param response:
        :return:
        """
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)
        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)

    def parse_detail(self, response):
        #title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first()
        # create_time = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first().strip().replace("·","").strip()
        # praise_number = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first()
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        # content = response.xpath("//div[@class='entry']").extract_first()
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        #article_item = JobboleArticleItem()
        # title = response.css("div.entry-header h1::text").extract_first()
        # create_time = response.css("p.entry-meta-hide-on-mobile::text").extract_first().strip().replace("·", "").strip()
        # praise_number = response.css("span.vote-post-up h10::text").extract_first()
        # fav_nums = response.css("span.bookmark-btn::text").extract_first()
        # fav_nums = re.findall("\d", fav_nums)
        # if fav_nums:
        #     fav_nums = fav_nums[0]
        # else:
        #     fav_nums = 0
        # comment_nums = response.css("a[href='#article-comment'] span::text").extract_first()
        # comment_nums = re.findall("\d", comment_nums)
        # if comment_nums:
        #     comment_nums = comment_nums[0]
        # else:
        #     comment_nums = 0
        # content = response.css("div.entry").extract_first()
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract_first()
        # tags = ",".join(tag_list)
        # article_item["title"] = title
        # article_item["create_time"] = create_time
        # article_item["url"] = response.url
        # article_item["praise_number"] = praise_number
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["content"] = content
        # article_item["front_image_url"] = [front_image_url]
        # article_item["tags"] = tags
        # article_item["url_object_id"] = get_md5(response.url)
        #itemloader 加载item
        # item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)
        # front_image_url = response.meta.get("front_image_url", "")
        # item_loader.add_css("title", "div.entry-header h1::text")
        # item_loader.add_value("front_image_url", [front_image_url])
        # item_loader.add_value("url", response.url)
        # item_loader.add_value("url_object_id", get_md5(response.url))
        # item_loader.add_css("praise_number", "span.vote-post-up h10::text")
        # item_loader.add_css("create_time", "p.entry-meta-hide-on-mobile::text")
        # item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        # item_loader.add_css("content", "div.entry")
        # item_loader.add_css("fav_nums", "span.bookmark-btn::text")
        # item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        # article_item = item_loader.load_item()
        # yield article_item
        item_loader = ArticleItemLoader(item=JobboleArticleItem(),response=response)
        front_image_url = response.meta.get("front_image_url","")
        item_loader.add_css("title","div.entry-header h1::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("praise_number", "span.vote-post-up h10::text")
        item_loader.add_css("create_time", "p.entry-meta-hider-on-mobile::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        item_loader.add_css("fav_nums", "span.bookmark-btn::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        article_item = item_loader.load_item()
        yield article_item



