# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from logging import getLogger
from scrapy.http import HtmlResponse
import time
# # useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter


class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome(service_args=service_args)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, 10)
        self.browser.get('https://www.jd.com/')
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_id('key').clear()
        self.browser.find_element_by_id('key').send_keys(self.settings.get('KEYWORD'))
        self.browser.find_element_by_class_name('button').click()

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        page = request.meta.get('page', 1)
        try:
            print('------------------------------------------------------------------------------------------------')
            print('正在抓取第', page, '页')

            if page > 1:
                self.browser.find_element_by_css_selector('.pn-next').click()
                self.browser.implicitly_wait(10)
                time.sleep(3)
                self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.p-num .curr'), str(page)))
            for i in range(1, 6):
                self.browser.execute_script("var action=document.documentElement.scrollTop={}".format(str(i*2000)))
                time.sleep(3)
            # goods = self.browser.find_elements_by_class_name('gl-item')
            # results = []
            # for good in goods:
            #     results.append(good.get_attribute('innerHTML'))
            results = self.browser.find_element_by_class_name('gl-warp').get_attribute('innerHTML')
            print(results)
            print('第', page, '页抓取完成')
            print('------------------------------------------------------------------------------------------------')
            return HtmlResponse(url=request.url, body=results, encoding='utf-8', status=200, request=request)
        except TimeoutException:
            print('第', page, '页抓取失败')
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'), service_args=crawler.settings.get('CHROME_SERVICE_ARGS'))


# class JingdongcrawlSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.

#         # Should return None or raise an exception.
#         return None

#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.

#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i

#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.

#         # Should return either None or an iterable of Request or item objects.
#         pass

#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn鈥檛 have a response associated.

#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r

#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


# class JingdongcrawlDownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.

#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None

#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.

#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response

#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.

#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass

#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
