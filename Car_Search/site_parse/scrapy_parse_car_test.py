
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import difflib
from car_obj import car_obj
import time

from parse_page_car import bs4_parse_car
from selenium_parse import selenium_parse

# logging.getLogger("scrapy").propagate = False
# logging.basicConfig(
#     level="INFO",
#     format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
#     datefmt="%d/%m/%Y %I:%M:%S %p",
# )

username = "kizy"
password = "dd5220-4902e5-ca7c78-712cbd-c377de"

PROXY_RACK_DNS = "usa.rotating.proxyrack.net:9000"
proxy = "http://cdfcd4e233464959ac5f1f8d45a9c05f:@proxy.crawlera.com:8011/"
timeout = 60
cat_timeout = 20

def handle_error(failure):
    pass

searched_car_list=[]


def normalized_str(s):
    normalized = s.lower()
    dict_symb=[' ','.',',','$','\n']
    for i in dict_symb:
        normalized=normalized.replace(i,'')
    return normalized

def similarity(s1, s2):
  normalized1 = normalized_str(s1)
  normalized2 = normalized_str(s2)
  matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
  return matcher.ratio()

def add_to_car_list(curr_car,search_car_list):

    similarity_title=similarity(normalized_str(curr_car.title),normalized_str(search_car_list.title))
    price_differense=int(normalized_str(search_car_list.price))-int(normalized_str(curr_car.price))

    if round(similarity_title,2)>=0.85 or str(curr_car.title).find(str(search_car_list.title))!=-1:
        if price_differense>=0:
            curr_car_info=curr_car.information.all_info
            search_car_list_info=search_car_list.info.all_info
            check_info=True
            for i in range (len(curr_car_info)):
                if curr_car_info[i].value!=None and search_car_list_info[i].value!=None:
                    if similarity(str(curr_car_info[i].value),str(search_car_list_info[i].value))<0.9:
                        check_info=False
            if check_info:
                searched_car_list.append(curr_car)


class car_Spider(scrapy.Spider):
    name = "automotoSpider"
    allowed_domains = ["automoto.ua"]
    not_allowed_keyword = ['/katalog','/book-new-auto','/newauto']
    check_ip_category = 0
    check_ip_article_links = 0
    start_urls = ['https://automoto.ua/uk/']
    search_list: car_obj.Search_List
    category_selector:str
    item_selector:str
    pagination_selector:str
    max_page_num:int
    links =[]


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
                    "link": i,
                }
            )

    def parse(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                categories_links = []
                res = response.css(self.category_selector)
                for r in res:
                    try:
                        if any(n in str(r.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if str(r.css("a").attrib["href"]) not in categories_links:
                                if "https://" in str(r.css("a").attrib["href"]) or "http://" in str(r.css("a").attrib["href"]):
                                    categories_links.append(r.css("a").attrib["href"])
                                else:

                                    categories_links.append(
                                        "https://automoto.ua" + r.css("a").attrib["href"]
                                    )

                    except:
                        pass

                for i in set(categories_links):
                    print(i)
                    try:
                        yield scrapy.Request(
                            i,
                            callback=self.article_links,
                            meta={"dont_retry": True, "download_timeout": cat_timeout,"base_url": response.url},
                            errback=handle_error,
                        )


                    except:
                        pass
        self.links.clear()

    def article_links(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css(self.item_selector)
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if link.css("a").attrib["href"] not in self.links:
                                if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(link.css("a").attrib["href"]):
                                    self.links.append(link.css("a").attrib["href"])
                                    try:
                                        yield scrapy.Request(
                                            link.css("a").attrib["href"],
                                            callback=self.get_info,
                                            meta={"dont_retry": True, "download_timeout": cat_timeout,
                                                  "base_url": response.url},
                                            errback=handle_error,
                                        )


                                    except:
                                        pass
                                else:
                                    self.links.append("https://automoto.ua" + link.css("a").attrib["href"])
                                    try:
                                        yield scrapy.Request(
                                            "https://automoto.ua" + link.css("a").attrib["href"],
                                            callback=self.get_info,
                                            meta={"dont_retry": True, "download_timeout": cat_timeout,
                                                  "base_url": response.url},
                                            errback=handle_error,
                                        )


                                    except:
                                        pass
                    except:
                        pass

                if response.css(self.pagination_selector):
                    if ('?page='+str(self.max_page_num)) not in response.url:
                        next_page = response.css('ul.pagination li:last-child a').attrib['href']
                        print(next_page)
                        if 'http' in next_page:
                            yield scrapy.Request(
                                next_page,
                                callback=self.article_links,
                                meta={"dont_retry": True, "download_timeout": cat_timeout, "base_url": response.url},
                                errback=handle_error,
                            )
                        else:
                            yield scrapy.Request(
                                "https://automoto.ua" + next_page,
                                callback=self.article_links,
                                meta={"dont_retry": True, "download_timeout": cat_timeout, "base_url": response.url},
                                errback=handle_error,
                            )



        else:
            while self.check_ip_category < 2:
                yield response.follow(self.start_urls[0], callback=self.start_requests_ip)
                self.check_ip_category += 1

    def get_info(self,response):
         curr_car = bs4_parse_car.automoto_parse_car_page(response.url)
         add_to_car_list(curr_car,self.search_list)






def start_parse_car_site(name,allowed_domains,not_allowed_keyword,start_urls,
                  search_list,category_selector,item_selector,pagination_selector,max_page_num):
    car_Spider.name = name
    car_Spider.allowed_domains = allowed_domains
    car_Spider.not_allowed_keyword = not_allowed_keyword
    car_Spider.start_urls = start_urls
    car_Spider.search_list = search_list
    car_Spider.category_selector = category_selector
    car_Spider.item_selector = item_selector
    car_Spider.pagination_selector = pagination_selector
    car_Spider.max_page_num = max_page_num
    #automotoSpider.search_list=search_list
    process = CrawlerProcess(settings={
                    "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
                    'FEED_EXPORT_FIELDS': ["url", "desc"],
                    "USER_AGENT" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
                })

    process.crawl(car_Spider)
    st = time.time()
    process.start()

    process.stop()
    print(f"this is total time {time.time()-st}")







car_char=car_obj.Car_Characteristics()

car_char.add_attr("Тип палива","Електро")
car_char.add_attr("Коробка","Автомат")
test_car_search=car_obj.Search_List("Volkswagen ","40 000 $",car_char,"в комплекті зимова гума, В ДТП не був торг біля капоту ")


start_parse_car_site("automotoSpider",["automoto.ua"], ['/katalog','/book-new-auto','/newauto'],['https://automoto.ua/uk/'],test_car_search,
                     '.dropdown:nth-child(6) .dropdown-item , .dropdown:nth-child(4) .dropdown-item , .d-lg-none+ .dropdown .dropdown-item',
                     '#item_list .stretched-link','ul.pagination li:last-child a',3)





#
# car=bs4_parse_car.automoto_parse_car_page("https://automoto.ua/uk/Audi-A4-2012-Vinnitsa-62586646.html")
#
# add_to_car_list(car,test_car_search)
#
for i in searched_car_list:
    print(i.link)

