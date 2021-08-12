import scrapy
from scrapy.http.request import Request
from jingdongcrawl.items import ProductItem
from pyquery import PyQuery as pq


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['www.jd.com']
    base_url = 'https://search.jd.com/Search?keyword='

    def start_requests(self):
        for page in range(1, 3):
            yield Request(url=self.base_url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        print('------------------------------------------------------------------------------------------------')
        print("正在解析：")
        html = response.body.decode('utf-8')
        print("response.body:" + html)
        doc = pq(html)
        goods = doc('li').items()
        for good in goods:
            item = ProductItem()
            item['name'] = good('.p-name em').text().replace('\n', ' ')
            item['price'] = good('.p-price i').text()
            item['shop'] = good('.p-shop a').text()
            item['link'] = 'https://' + good('.p-name a').attr('href')
            yield item
