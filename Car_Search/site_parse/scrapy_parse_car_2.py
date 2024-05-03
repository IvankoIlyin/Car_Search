import time
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import datetime


logging.getLogger("scrapy").propagate = False
logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)
username = "kizy"
password = "dd5220-4902e5-ca7c78-712cbd-c377de"

PROXY_RACK_DNS = "usa.rotating.proxyrack.net:9000"
proxy = "http://cdfcd4e233464959ac5f1f8d45a9c05f:@proxy.crawlera.com:8011/"
timeout = 60
cat_timeout = 20

def handle_error(failure):
    pass


class ScrapyParseCarSpider(scrapy.Spider):
    name = "scrapy_parse_car"
    allowed_domains = ["m.rst.ua"]
    start_urls = ["https://m.rst.ua/"]

    def parse(self, response):
        print(2)

class OxfordBusinessGroupSpider(scrapy.Spider):
    name = "OxfordBusinessGroupSpider"
    allowed_domains = ["oxfordbusinessgroup.com"]
    not_allowed_keyword = []
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://oxfordbusinessgroup.com/explore-market-research/africa/algeria/']

    def start_requests(self):
        for i in self.start_urls:
            res = scrapy.Request(
                i,
                callback=self.parse,
                dont_filter=True,
                meta={"dont_retry": True, "download_timeout": timeout},
                errback=handle_error,
            )
            yield res

    def start_requests_ip(self, arg):
        for i in self.start_urls:
            res_ip = scrapy.Request(
                i,
                meta={"proxy": proxy, "dont_retry": True, "download_timeout": timeout},
                callback=self.parse,
                dont_filter=True,
                errback=handle_error,
            )
            yield res_ip
        logging.info(
            {
                "proxy": "1",
                "clean_url": self.allowed_domains[0],
                "link": self.start_urls,
            }
        )

    def parse(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.entry-title a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if "https://" in str(link.css("a").attrib["href"]):
                                print(link.css("a").attrib["href"])
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": link.css("a").attrib["href"],
                                       }

                            else:
                                yield {"clean_url": self.allowed_domains[0],
                                       "base_url": response.url,
                                       "link": "https://oxfordbusinessgroup.com" + link.css("a").attrib["href"],
                                       }

                    except:
                        pass



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1




process = CrawlerProcess(settings={
                'FEEDS':{f"Newlink_1.json":{'format': 'json','overwrite': True}},
                "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
                'FEED_EXPORT_FIELDS': ["url", "desc"],
                # "FEED_URI" : f"Newlink_1.json",
                # "FEED_FORMAT" : "json",
                "USER_AGENT" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
            })

process.crawl(OxfordBusinessGroupSpider)
st = time.time()
process.start()

process.stop()
print(f"this is total time {time.time()-st}")