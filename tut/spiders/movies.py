#-*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urlparse import urljoin

from tut.items import MoviesItem

class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["imdb.com"]
    start_urls = [
        "http://www.imdb.com/chart/top?ref_=nv_ch_250_4"
    ]

    def parse(self, response):
        for href in response.xpath('//*[contains(@*,"lister-list")]//tr//a/@href').extract():
        	url = urljoin(response.url,href)
        	yield Request(url, callback=self.parse_dir_contents)


    def parse_dir_contents(self, response):
    	item = MoviesItem()
    	item['desc'] = response.xpath('//table//tbody//tr[1]/td/p/text()').extract()
    	item['title'] = response.xpath('//h1[@class="header"]//span[@class="itemprop"]/text()').extract()
    	item['img'] = response.xpath('//div[@class="image"]//a//img/@src').extract()
    	yield item