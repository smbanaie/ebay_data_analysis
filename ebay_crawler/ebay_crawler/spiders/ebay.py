# -*- coding: utf-8 -*-
from ebay_crawler.items import EbayCrawlerItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import codecs
import os
from datetime import datetime


class EbaySpider(CrawlSpider):
    name = 'ebay'
    allowed_domains = ['ebay.com.au']
    start_urls = [
        r"https://www.ebay.com.au/b/Refrigerators/20713/bn_2210468",
        r"https://www.ebay.com.au/b/Mini-Refrigerators/71262/bn_100359265"
    ]
    fridges_details = r"fridges_info"
    data_dir = "data"

    def __init__(self):
        super().__init__()
        if not os.path.exists(self.data_dir + os.path.sep +self.fridges_details + datetime.now()
                .strftime("-%Y-%m") + '.csv'):
            self.write_fridges_info({}, header=True)

    rules = [
                Rule(LinkExtractor(allow=r'/itm/', ), callback='parse_ads', follow=False),
                Rule(LinkExtractor(allow=[r'/b/Mini-Refrigerators/.*_pgn=\d+',
                                          r'/b/Refrigerators/.*_pgn=\d+'], ), follow=True)
             ]
    # logger = logging.getLogger(__name__)

    def parse_ads(self, response):
        item = EbayCrawlerItem()
        item["id"] = response.request.url.split("/")[5].split("?")[0]
        item["url"] = response.request.url
        item["model"] = response.xpath(
            '//div[@class="itemAttr"]//td[.//text()[contains(.,"Model:")]]/following-sibling::td[1]/span/text()').get()
        item["brand"] = response.xpath(
            '//div[@class="itemAttr"]//td[.//text()[contains(.,"Brand:")]]/following-sibling::td[1]/span/text()').get()
        item["capacity"] = response.xpath(
            '//div[@class="itemAttr"]//td[.//text()[contains(.,"Capacity:")]]/following-sibling::td[1]/span/text()')\
            .get()
        item["condition"] = response.css(".condText::text").get()
        item["location"] = response.xpath("//span[@itemprop='availableAtOrFrom']/text()").get()
        item["price"] = response.xpath("//span[@id='prcIsum']").xpath("./@content").get()
        item["delivery_time"] = response.css('.vi-acc-del-range b::text').get()

        self.write_fridges_info(item)
        yield item

    def write_fridges_info(self, item, header=False):
        f = codecs.open(self.data_dir + os.path.sep +self.fridges_details + datetime.now()
                        .strftime("-%Y-%m") + '.csv', "a", encoding="utf8")
        if not header:
            row_csv = "{0},{1},{2},{3},{4},{5},{6},{7},{8}\r\n".format(
                item["id"],
                item["model"].replace(",", "^") if item["model"] is not None else item["model"],
                item["brand"].replace(",", "^") if item["brand"] is not None else item["brand"],
                item["capacity"].replace(",", "^") if item["capacity"] is not None else item["capacity"],
                item["condition"].replace(",", "^") if item["condition"] is not None else item["condition"],
                item["location"].replace(",", "^") if item["location"] is not None else item["location"],
                item["price"].replace(",", "^") if item["price"] is not None else item["price"],
                item["delivery_time"].replace(",", "^") if item["delivery_time"] is not None else item["delivery_time"],
                item["url"],
            )
        else:
            row_csv = "{0},{1},{2},{3},{4},{5},{6},{7},{8}\r\n".format("ID", "Model", "Brand", "Capacity", "Condition",
                                                                       "Location", "Price", "Delivery Time", "URL")
        f.write(row_csv)
        f.close()

