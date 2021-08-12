import scrapy
from urllib.parse import quote
from scrapy.http.request import Request
from jingdongcrawl.items import ProductItem
from pyquery import PyQuery as pq


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['www.jd.com']
    base_url = 'https://search.jd.com/Search?keyword='

    def start_requests(self):
        for page in range(1, 3):
            url = self.base_url + quote(self.settings.get('KEYWORD'))
            yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        result = pq(response)
        item = ProductItem()
        item['name'] = result('.p-name em').text().replace('\n', ' '),
        item['price'] = result('.p-price i').text(),
        item['shop'] = result('.p-shop a').text(),
        item['link'] = result('.p-name a').attr('href')
        yield item
        # doc = pq(response)
        # results = doc
        # for result in results:
        #     item = ProductItem()
        #     item['name'] = result('.p-name em').text().replace('\n', ' '),
        #     item['price'] = result('.p-price i').text(),
        #     item['shop'] = result('.p-shop a').text(),
        #     item['link'] = result('.p-name a').attr('href')
        #     yield item
        # results = response
        # for result in results:
        #     doc = pq(result)
        #     item = ProductItem()
        #     item['name'] = doc('.p-name em').text().replace('\n', ' '),
        #     item['price'] = doc('.p-price i').text(),
        #     item['shop'] = doc('.p-shop a').text(),
        #     item['link'] = doc('.p-name a').attr('href')
        #     yield item
