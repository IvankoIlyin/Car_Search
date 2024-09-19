import asyncio

import scrapy
from scrapy.crawler import CrawlerProcess
from concurrent.futures import ProcessPoolExecutor

import difflib
from car_obj import car_obj
import math
from parse_page_car import bs4_parse_car
from selenium_parse import selenium_parse

timeout = 60
short_timeout = 20

settings = {
    "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


# help method
def is_list_empty(l) -> bool:
    if not l or l is None:
        return True
    else:
        return False


def check_list_int_str(l):
    for i in l:
        if get_int_from_str(i) == None:
            return False
        else:
            return True


def erase_alpha(s):
    return ''.join(i for i in s if not i.isalpha())


def normalized_str(s):
    normalized = s.lower()
    dict_symb = [' ', '.', ',', '$', '\n', '\xa0']
    for i in dict_symb:
        normalized = normalized.replace(i, '')
    return normalized


def similarity(s1, s2):
    normalized1 = normalized_str(s1)
    normalized2 = normalized_str(s2)
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


def get_int_from_str(s):
    try:
        return int(erase_alpha(normalized_str(s)))
    except:
        return None


def max_list(l):
    int_l = []
    for i in l:
        int_l.append(get_int_from_str(i))
    return max(int_l)


def similarity_list_str(l1, l2):
    sim_flag = True
    if is_list_empty(l1) == False and is_list_empty(l2) == False:
        if check_list_int_str(l1) == False and check_list_int_str(l2) == False:
            sim_flag = False
            l1_data, l2_data = "", ""
            for i in l1:
                l1_data += str(i)
            for i in l2:
                l2_data += str(i)
            if similarity(l1_data, l2_data) >= 0.7 or l1_data in l2 or l2_data in l1:
                sim_flag = True

            for i in l2:
                if l1_data.find(i) != -1:
                    sim_flag = True

    return sim_flag


def check_car_name(title, mark, model):
    title = normalized_str(title).strip()

    mark = normalized_str(mark).strip()
    model = normalized_str(model).strip()

    return mark in title and model in title


def check_price(curr_car, search_car: car_obj.Car):
    if search_car.price[0] == '' and search_car.price[1] == '':
        return True
    if search_car.price[0] == '' and get_int_from_str(curr_car.price) <= get_int_from_str(search_car.price[1]):
        return True
    if search_car.price[1] == '' and get_int_from_str(curr_car.price) >= get_int_from_str(search_car.price[0]):
        return True
    if search_car.price[0] != '' and search_car.price[1] != '' and get_int_from_str(curr_car.price) >= get_int_from_str(
            search_car.price[0]) and get_int_from_str(
            curr_car.price) <= get_int_from_str(search_car.price[1]):
        return True

    return False


def check_year(curr_car, search_car: car_obj.Car):
    if search_car.year[0] == "" and search_car.year[1] == "":
        return True

    if search_car.year[0] == "" and get_int_from_str(curr_car.year) <= get_int_from_str(search_car.year[1]):
        return True

    if search_car.year[1] == "" and get_int_from_str(curr_car.year) >= get_int_from_str(search_car.year[0]):
        return True

    if search_car.year[0] != "" and search_car.year[1] != "" and get_int_from_str(curr_car.year) >= get_int_from_str(
            search_car.year[0]) and get_int_from_str(curr_car.year) <= get_int_from_str(search_car.year[1]):
        return True

    return False


def add_to_car_list(curr_car, search_car: car_obj.Car, searched_car_list):
    if check_car_name(curr_car.title, search_car.mark, search_car.model) == True or similarity(curr_car.title,
                                                                                               search_car.mark + search_car.model) >= 0.6:
        print('title is good')
        if check_price(curr_car, search_car) == True:
            print("price is good")
            if check_year(curr_car, search_car) == True:
                curr_car_info = curr_car.information.all_info
                search_car_info = search_car.characteristics.all_info
                check_info = True
                print("Checking char")
                for i in range(len(curr_car_info)):

                    if similarity_list_str(curr_car_info[i].value, search_car_info[i].value) != True:
                        check_info = False
                        print("Bad")

                if check_info == True:
                    searched_car_list.append(curr_car)


def split_string(s, n):
    part_length = len(s) // n
    remainder = len(s) % n
    return [s[i * part_length + min(i, remainder):(i + 1) * part_length + min(i + 1, remainder)] for i in range(n)]


def similarity_descr(curr, search):
    percent = 0
    if (curr != None and search != None) and (curr != '' and search != '') and (len(curr) != 0 and len(search) != 0):
        if len(normalized_str(curr)) == len(normalized_str(search)):
            percent = similarity(curr, search)

        if len(normalized_str(curr)) > len(normalized_str(search)):
            list = split_string(curr, math.floor(len(curr) / len(search)))
            for i in list:
                percent += similarity(search, i)

        if len(normalized_str(search)) > len(normalized_str(curr)):
            list = split_string(curr, math.floor(len(search) / len(curr)))
            for i in list:
                percent += similarity(curr, i)
    return percent


def sort_list_by_description(list, search_description):
    n = len(list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if similarity_descr(list[j].description, search_description.dedescription) < similarity_descr(
                    list[j + 1].description, search_description.dedescription):
                list[j], list[j + 1] = list[j + 1], list[j]

    return list


# Spiders
class Car_automoto_Parse_Spider(scrapy.Spider):
    name = "automotoSpider"
    allowed_domains = ["automoto.ua"]
    not_allowed_keyword = ['/katalog', '/book-new-auto', '/newauto']
    search_list: car_obj.Search_List
    start_urls = []
    searched_car_list = []
    links = []
    page_count = 0
    curr_page_link = []

    def start_requests(self):
        for i in self.start_urls:
            res = scrapy.Request(
                i,
                callback=self.parse,
                dont_filter=True,
                meta={"dont_retry": True, "download_timeout": timeout}
            )
            yield res

    def parse(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('#item_list .stretched-link')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if link.css("a").attrib["href"] not in self.links:
                                if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(
                                        link.css("a").attrib["href"]):
                                    self.links.append(link.css("a").attrib["href"])
                                    try:
                                        yield scrapy.Request(
                                            link.css("a").attrib["href"],
                                            callback=self.get_info,
                                            meta={"dont_retry": True, "download_timeout": short_timeout},
                                        )
                                    except:
                                        pass
                                else:
                                    self.links.append("https://automoto.ua" + link.css("a").attrib["href"])
                                    try:
                                        yield scrapy.Request(
                                            "https://automoto.ua" + link.css("a").attrib["href"],
                                            callback=self.get_info,
                                            meta={"dont_retry": True, "download_timeout": short_timeout},
                                        )


                                    except:
                                        pass
                    except:
                        pass

                if response.css('ul.pagination li:last-child a'):
                    next_page = response.css('ul.pagination li:last-child a').attrib['href']
                    print(next_page)
                    self.curr_page_link.append("https://automoto.ua" + next_page)
                    if self.page_count <= 3:
                        if 'http' in next_page:
                            yield scrapy.Request(
                                next_page,
                                callback=self.parse,
                                meta={"dont_retry": True, "download_timeout": timeout},
                            )
                        else:
                            yield scrapy.Request(
                                "https://automoto.ua" + next_page,
                                callback=self.parse,
                                meta={"dont_retry": True, "download_timeout": timeout},
                            )
                        self.page_count += 1
                        self.curr_page_link.clear()
                if not response.css('ul.pagination li:last-child a'):
                    self.curr_page_link.clear()

    def get_info(self, response):
        curr_car = bs4_parse_car.automoto_parse_car_page(response.url)
        add_to_car_list(curr_car, self.search_list, self.searched_car_list)


class Car_autoria_Parse_Spider(scrapy.Spider):
    name = "autoriaSpider"
    allowed_domains = ["auto.ria.com"]
    not_allowed_keyword = []
    start_url = None
    start_urls = [start_url]
    search_list: car_obj.Search_List
    searched_car_list = []
    links = []
    page_count = 0
    curr_page_link = []

    def start_requests(self):
        for i in self.start_urls:
            res = scrapy.Request(
                i,
                callback=self.parse,
                dont_filter=True,
                meta={"dont_retry": True, "download_timeout": timeout},
            )
            yield res

    def parse(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('.item.ticket-title a.address')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if link.css("a").attrib["href"] not in self.links:
                                if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(
                                        link.css("a").attrib["href"]):
                                    self.links.append(link.css("a").attrib["href"])
                                    try:
                                        yield scrapy.Request(
                                            link.css("a").attrib["href"],
                                            callback=self.get_info,
                                            meta={"dont_retry": True, "download_timeout": short_timeout}
                                        )


                                    except:
                                        pass
                                else:
                                    self.links.append("https://auto.ria.com" + link.css("a").attrib["href"])
                                    try:
                                        yield scrapy.Request(
                                            "https://auto.ria.com" + link.css("a").attrib["href"],
                                            callback=self.get_info,
                                            meta={"dont_retry": True, "download_timeout": short_timeout}
                                        )


                                    except:
                                        pass
                    except:
                        pass

                if response.css('.page-link.js-next'):
                    next_page = response.css('.page-link.js-next').attrib['href']
                    print(next_page)
                    print(self.page_count)
                    self.curr_page_link.append("https://auto.ria.com" + next_page)
                    if self.page_count <= 3:
                        if 'http' in next_page:
                            yield scrapy.Request(
                                next_page,
                                callback=self.parse,
                                meta={"dont_retry": True, "download_timeout": timeout}
                            )
                        else:
                            yield scrapy.Request(
                                "https://auto.ria.com" + next_page,
                                callback=self.parse,
                                meta={"dont_retry": True, "download_timeout": timeout}
                            )
                        self.page_count += 1
                        self.curr_page_link.clear()

                if not response.css('.page-link.js-next'):
                    self.curr_page_link.clear()

    def get_info(self, response):
        curr_car = bs4_parse_car.autoria_parse_car_page(response.url)
        add_to_car_list(curr_car, self.search_list, self.searched_car_list)


class Car_dexpens_Parse_Spider(scrapy.Spider):
    name = "dexpensSpider"
    allowed_domains = ["dexpens.com"]
    not_allowed_keyword = []
    start_url = None
    start_urls = [start_url]
    search_list: car_obj.Search_List
    links = []

    def start_requests(self):
        for i in self.start_urls:
            res = scrapy.Request(
                i,
                callback=self.parse,
                dont_filter=True,
                meta={"dont_retry": True, "download_timeout": timeout}
            )
            yield res

    def parse(self, response):
        if str(response.status) == "200":
            if response.css("body"):
                data = response.css('#autoMarketTab a')
                for link in data:
                    try:
                        if any(n in str(link.css("a").attrib["href"]) for n in self.not_allowed_keyword):
                            pass
                        else:
                            if link.css("a").attrib["href"] not in self.links:
                                if "https://" in str(link.css("a").attrib["href"]) or "http://" in str(
                                        link.css("a").attrib["href"]):
                                    self.links.append(link.css("a").attrib["href"])
                                    try:
                                        yield scrapy.Request(
                                            link.css("a").attrib["href"],
                                            callback=self.get_info,
                                            meta={"dont_retry": True, "download_timeout": short_timeout}
                                        )


                                    except:
                                        pass
                                else:
                                    self.links.append("https://www.dexpens.com" + link.css("a").attrib["href"])
                                    try:
                                        yield scrapy.Request(
                                            "https://www.dexpens.com" + link.css("a").attrib["href"],
                                            callback=self.get_info,
                                            meta={"dont_retry": True, "download_timeout": short_timeout}
                                        )


                                    except:
                                        pass
                    except:
                        pass

                if response.css('#bottom-nav .pagination-panel a:last-child'):
                    next_page = response.css('.pagination-panel a:last-child').attrib['href']
                    print(next_page)
                    if 'http' in next_page:
                        yield scrapy.Request(
                            next_page,
                            callback=self.parse,
                            meta={"dont_retry": True, "download_timeout": timeout}
                        )
                    else:
                        yield scrapy.Request(
                            "https://www.dexpens.com" + next_page,
                            callback=self.parse,
                            meta={"dont_retry": True, "download_timeout": timeout}
                        )

    def get_info(self, response):
        curr_car = bs4_parse_car.dexpens_parse_car_page(response.url)
        add_to_car_list(curr_car, self.search_list)


# Run_All
def start_parse_car_site(search_list):
    process = CrawlerProcess(settings=settings)

    start_url_automoto = selenium_parse.selenium_parse_automoto(search_list)
    Car_automoto_Parse_Spider.start_urls = [start_url_automoto]
    Car_automoto_Parse_Spider.search_list = search_list

    start_url_autoria = selenium_parse.selenium_parse_autoria(search_list)
    Car_autoria_Parse_Spider.start_urls = [start_url_autoria]
    Car_autoria_Parse_Spider.search_list = search_list

    process.crawl(Car_autoria_Parse_Spider)
    process.crawl(Car_automoto_Parse_Spider)
    process.start()

    list = Car_automoto_Parse_Spider.searched_car_list + Car_autoria_Parse_Spider.searched_car_list
    # list = Car_automoto_Parse_Spider.searched_car_list
    list = sort_list_by_description(list, search_list)

    curr_url_automoto = Car_automoto_Parse_Spider.curr_page_link
    try:
        curr_url_automoto = curr_url_automoto[0]
    except:
        curr_url_automoto = ''

    curr_url_autoria = Car_autoria_Parse_Spider.curr_page_link
    try:
        curr_url_autoria = curr_url_autoria[0]
    except:
        curr_url_autoria = ''

    process.stop()
    return list, [curr_url_automoto, curr_url_autoria]


def continue_parse_car_site(search_list, curr_start_url):
    process = CrawlerProcess(settings=settings)

    if curr_start_url[0] != '':
        Car_automoto_Parse_Spider.start_urls = [curr_start_url[0]]
        Car_automoto_Parse_Spider.search_list = search_list
        process.crawl(Car_automoto_Parse_Spider)

    if curr_start_url[1] != '':
        Car_autoria_Parse_Spider.start_urls = [curr_start_url[1]]
        Car_autoria_Parse_Spider.search_list = search_list
        process.crawl(Car_autoria_Parse_Spider)

    process.start()

    list = Car_automoto_Parse_Spider.searched_car_list + Car_autoria_Parse_Spider.searched_car_list
    list = sort_list_by_description(list, search_list)

    curr_url_automoto = Car_automoto_Parse_Spider.curr_page_link
    try:
        curr_url_automoto = curr_url_automoto[0]
    except:
        curr_url_automoto = ''

    curr_url_autoria = Car_autoria_Parse_Spider.curr_page_link
    try:
        curr_url_autoria = curr_url_autoria[0]
    except:
        curr_url_autoria = ''

    process.stop()

    return list, [curr_url_automoto, curr_url_autoria]

# char=car_obj.Car_Characteristics()
# # char.add_attr("Коробка","Механіка")
# # char.add_attr("Коробка","Автомат")
# # char.add_attr("Паливо","Бензин")
# # char.add_attr("Паливо","Дизель")
# # char.add_attr("Двигун","2")
# # char.add_attr("Кузов","Седан")
# # char.add_attr("Пробіг","300")
# # char.add_attr("Привід","Передній")
#
# car=car_obj.Car("Audi","A4",["3000","7000"],["2000","2010"],char,"Топ")

# char.display_all_characteristics()
