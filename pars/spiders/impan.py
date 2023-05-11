import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class FianItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field

class NatureSpider(CrawlSpider):
    name = 'impan1'

    custom_settings = {
        'FILES_STORE': "data/" + name,
        'LOG_FILE': "log/" + name + ".log",
        'DOWNLOAD_DELAY': 0.3,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'MEDIA_ALLOW_REDIRECTS': True,
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 0,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [301, 302, 403],
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
    }
    allowed_domains = ['impan.pl']
    start_urls = ['https://www.impan.pl/en/publishing-house/journals-and-series']

    rules = (
    Rule(LinkExtractor(allow=('.+\/en\/publishing-house\/journals-and-series\/\D+'),
                       deny='.*online.*'),
    callback='parse', follow=True),

    Rule(LinkExtractor(allow='.+\/en\/publishing-house\/journals-and-series\/\D+\/all\/\d+\/\d'),
    callback='parse', follow=True),
    )

    def parse(self, response):
        urls = []
        s = response.xpath('//div[@class="info"]/a')
        if (s):
          for i in s:
            urls.append(response.urljoin(i.attrib['href']))
        else:
          return
        item = FianItem()
        item['file_urls'] = urls
        yield item
