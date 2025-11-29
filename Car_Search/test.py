import unittest
import sys
from unittest.mock import patch, MagicMock
# Прибрано повторний імпорт car_obj
import time
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import asyncio

import scrapy
from scrapy.crawler import CrawlerProcess
from concurrent.futures import ProcessPoolExecutor

import difflib
import math

# Set path for module import (це вже є, але для структури пакетів потрібні точні шляхи)
sys.path.insert(0, '.')

# --- Direct imports of project modules (ВИПРАВЛЕНО ШЛЯХИ) ---
# car_obj.py знаходиться в car_obj/
from car_obj.car_obj import Car, Car_Characteristics, car_obj
# questions.py знаходиться в handlers/
from handlers.questions import (
    check_price, check_year, split_car_name, extract_year, extract_price,
    price_year, normalize_attr, add_list_attr, count_char
)
# scrapy_parse_car.py знаходиться в site_parse/
from site_parse.scrapy_parse_car import (
    is_list_empty, check_list_int_str, erase_alpha, normalized_str, similarity,
    get_int_from_str, max_list, similarity_list_str, check_car_name,
    check_price as check_price_scrapy, check_year as check_year_scrapy,
    add_to_car_list, split_string, similarity_descr, sort_list_by_description
)
# bs4_parse_car.py знаходиться в parse_page_car/
from parse_page_car.bs4_parse_car import (
    extract_year as extract_year_bs4, automoto_parse_car_page,
    autoria_parse_car_page, dexpens_parse_car_page
)
# --- End of project module imports ---


# --- Mock data for BS4 parsing testing ---

# Mock HTML response for automoto_parse_car_page
AUTOMOTO_MOCK_HTML = """
<html>
<body>
    <h1 class="main-card-name">Audi A4 2012 Sedan (Вінниця)</h1>
    <div class="price-item">10 500 $</div>
    <div class="pb-0">
        <div class="px-md-0">
            <p>Чудовий автомобіль для міста.</p>
            <p>Обслуговувався вчасно.</p>
        </div>
    </div>
    <div class="py-md-0">
        <table>
            <tbody>
                <tr><td>Тип кузова</td><td>Седан</td></tr>
                <tr><td>Двигун</td><td>2.0 л (Дизель)</td></tr>
                <tr><td>КПП</td><td>Автомат</td></tr>
            </tbody>
        </table>
    </div>
</body>
</html>
"""

# Mock HTML response for autoria_parse_car_page
AUTORIA_MOCK_HTML = """
<html>
<body>
    <h1 class="head">Audi A4 2015 2.0 (Бензин)</h1>
    <div class="price_value"><strong>12 000</strong></div>
    <div class="full-description">Продаю своє авто. Ніколи не підводило.</div>
    <dl id="details">
        <dd>Седан • 5 місць</dd>
        <div class="description-car">
            <dl class="technical-info">
                <dd><span class="label">Двигун</span> <span class="argument">2.0 л • Бензин</span></dd>
                <dd><span class="label">Коробка передач</span> <span class="argument">Автомат</span></dd>
            </dl>
        </div>
    </dl>
</body>
</html>
"""

# Mock HTML response for dexpens_parse_car_page
DEXPENS_MOCK_HTML = """
<html>
<body>
    <h1 class="car-name-sell">Skoda Octavia 2003</h1>
    <h2 class="advertisement-price auto-pr">3500 $ / 3200 €</h2>
    <div class="other-description-car">Надійний та економний.</div>
    <div class="padding-bottom-12">
        <div><div><span>250 тис. км</span></div></div>
    </div>
    <div class="position-relative">
        <div class="row">
            <div class="col-md-4"><label>Паливо</label></div>
            <div class="col-md-8">Дизель</div>
        </div>
        <div class="row">
            <div class="col-md-4"><label>Колір</label></div>
            <div class="col-md-8">Синій</div>
        </div>
    </div>
</body>
</html>
"""

class TestCarObject(unittest.TestCase):
    """Testing classes from car_obj.py."""

    def test_car_characteristics_add_attr_success(self):
        char = Car_Characteristics()
        char.add_attr("Тип кузова", "Седан")
        self.assertIn("Седан", char.body_type.value)

        # Check synonyms
        char.add_attr("КПП", "Механіка")
        self.assertIn("Механіка", char.transmission.value)

        # Check uniqueness
        char.add_attr("Колір", "Чорний")
        char.add_attr("Колір", "Чорний")
        self.assertEqual(char.color.value, ["Чорний"])

        # Check that adding an attribute not in keys correctly leads to its absence in other fields
        char.add_attr("Невідповідний ключ", "Значення")
        self.assertTrue("Значення" not in char.color.value)

    def test_car_characteristics_clear_success(self):
        char = Car_Characteristics()
        char.add_attr("Пробіг", "100")
        char.clear()
        self.assertEqual(char.mileage.value, [])

    def test_car_characteristics_check_empty_expected(self):
        char = Car_Characteristics()
        # Initial state: All 8 characteristics are empty
        self.assertEqual(char.check_empty(), 8)

        char.add_attr("Коробка", "Автомат")
        # Expected state: 7 characteristics remain empty
        self.assertEqual(char.check_empty(), 7)

    def test_car_obj_initialization_success(self):
        car = car_obj(title="Test", price="1000", year="2020", link="http://test.com")
        self.assertEqual(car.title, "Test")
        self.assertEqual(car.link, "http://test.com")

    def test_search_car_initialization_success(self):
        char = Car_Characteristics()
        car = Car(mark="Audi", model="A4", price=["1000", "5000"], year=["2000", "2010"], characteristic=char, dedescription="Топ")
        self.assertEqual(car.mark, "Audi")
        self.assertEqual(car.dedescription, "Топ")


class TestUtilityFunctions(unittest.TestCase):
    """Testing utility functions from questions.py."""

    def test_check_price_order_success(self):
        self.assertEqual(check_price(["1000", "5000"]), ["1000", "5000"])
        self.assertEqual(check_price(["5000", "1000"]), ["1000", "5000"])

    def test_check_year_order_success(self):
        self.assertEqual(check_year(["2000", "2010"]), ["2000", "2010"])
        self.assertEqual(check_year(["2010", "2000"]), ["2000", "2010"])
        self.assertEqual(check_year(["2005", "2005"]), ["2005", ""])

    def test_split_car_name_success(self):
        self.assertEqual(split_car_name("Audi A4"), ("Audi", "A4"))
        self.assertEqual(split_car_name("Land Rover Discovery Sport"), ("Land", "Rover Discovery Sport"))
        # Check expected output for invalid input (positive check on behavior)
        self.assertEqual(split_car_name(".."), ("", ""))

    def test_price_year_extraction_success(self):
        self.assertEqual(price_year("1000-5000"), ["1000", "5000"])
        self.assertEqual(price_year("2000, 2010.5000 10000"), ["2000", "2010", "5000", "10000"])
        self.assertEqual(price_year("From $1000 to $5000"), ["1000", "5000"])

    def test_normalize_attr_success(self):
        self.assertEqual(normalize_attr("  АВТОМАТ "), "Автомат")
        self.assertEqual(normalize_attr("меХанІка"), "Механіка")

    def test_add_list_attr_success(self):
        char = Car_Characteristics()
        char = add_list_attr('Паливо', "БЕНЗИН, ДИЗЕЛЬ, Пропустити", char)
        self.assertIn("Бензин", char.fuel_type.value)
        self.assertIn("Дизель", char.fuel_type.value)
    def test_count_char_sufficient_data_success(self):
        # Test case where data is sufficient (returns True)
        char = Car_Characteristics()
        char.add_attr("Продавець", "Власник")
        char.add_attr("Коробка", "Автомат")
        char.add_attr("Паливо", "Бензин")
        char.add_attr("Привід", "Передній")
        char.add_attr("Кузов", "Седан")
        car = Car("Audi", "A4", ["3000", "5000"], ["2000", "2010"], char, "Опис")
        self.assertTrue(count_char(car))

    def test_count_char_insufficient_data_expected_failure(self):
        # Test case where data is insufficient (returns False)
        char = Car_Characteristics()
        char.add_attr("Продавець", "Власник")
        char.add_attr("Коробка", "Автомат")
        car = Car("Audi", "A4", ["", ""], ["", ""], char, "Опис")
        # Check that the function correctly returns False (positive check on behavior)
        self.assertEqual(count_char(car), False)


class TestScrapyLogic(unittest.TestCase):
    """Testing utility functions from scrapy_parse_car.py."""

    def setUp(self):
        self.search_car_char = Car_Characteristics()
        self.search_car_char.add_attr("Паливо", "Бензин")
        self.search_car_char.add_attr("Коробка", "Автомат")
        self.search_car = Car("Audi", "A4", ["5000", "10000"], ["2005", "2015"], self.search_car_char, "Надійний")

    def test_is_list_empty_success(self):
        self.assertTrue(is_list_empty([]))
        self.assertTrue(is_list_empty(None))
        self.assertTrue(not is_list_empty(["a"]))

    def test_similarity_success(self):
        self.assertAlmostEqual(similarity("audi a4", "Audi A4"), 1.0)
        # Check that similarity is correctly low (positive check on behavior)
        self.assertTrue(similarity("audi a4", "bmw x5") < 0.5)

    def test_get_int_from_str_success(self):
        self.assertEqual(get_int_from_str("10 500 $"), 10500)
        # Check that failure correctly returns None (positive check on behavior)
        self.assertIs(get_int_from_str("test"), None)

    def test_check_car_name_match_success(self):
        self.assertTrue(check_car_name("Audi A4 2010", "Audi", "A4"))
        # Check that no match correctly returns False (positive check on behavior)
        self.assertEqual(check_car_name("Audi A3 2010", "Audi", "A4"), False)

    def test_check_price_scrapy_in_range_success(self):
        curr_car = car_obj(price="7500")
        self.assertTrue(check_price_scrapy(curr_car, self.search_car))
        # Check that out of range correctly returns False (positive check on behavior)
        curr_car = car_obj(price="15000")
        self.assertEqual(check_price_scrapy(curr_car, self.search_car), False)

    def test_check_year_scrapy_in_range_success(self):
        curr_car = car_obj(year="2010")
        self.assertTrue(check_year_scrapy(curr_car, self.search_car))
        # Check that out of range correctly returns False (positive check on behavior)
        curr_car = car_obj(year="2020")
        self.assertEqual(check_year_scrapy(curr_car, self.search_car), False)

    def test_similarity_list_str_match_success(self):
        self.assertTrue(similarity_list_str([], []))
        self.assertTrue(similarity_list_str(["1"], ["1"]))
        self.assertTrue(similarity_list_str(["автомат", "робот"], ["автомат робот"]))
        # Check that no match correctly returns False (positive check on behavior)
        self.assertEqual(similarity_list_str(["Бензин"], ["Дизель"]), False)

    def test_add_to_car_list_success(self):
        curr_car_char = Car_Characteristics()
        curr_car_char.add_attr("Паливо", "Бензин")
        curr_car_char.add_attr("Коробка", "Автомат")
        curr_car = car_obj(title="Audi A4 2010", price="7000", year="2010", information=curr_car_char)

        searched_list = []
        add_to_car_list(curr_car, self.search_car, searched_list)
        self.assertEqual(len(searched_list), 1)

    def test_sort_list_by_description_success(self):
        car1 = car_obj(description="Надійний автомобіль, без проблем.")
        car2 = car_obj(description="Автомобіль, який потребує ремонту.")

        search_car = Car(dedescription="Надійний")

        sorted_list = sort_list_by_description([car2, car1], search_car)
        self.assertEqual(sorted_list[0].description, "Надійний автомобіль, без проблем.")


class TestBs4Parsing(unittest.TestCase):
    """
    Testing parsing functions from bs4_parse_car.py.
    External HTTP requests are mocked using unittest.mock.
    """

    @patch('requests.get')
    def test_automoto_parse_car_page_success(self, mock_get):
        # Configure mock object to simulate requests.get response
        mock_response = MagicMock()
        mock_response.content = AUTOMOTO_MOCK_HTML.encode('utf-8')
        mock_get.return_value = mock_response

        link = "http://automoto.ua/test-link"
        car = automoto_parse_car_page(link)

        self.assertEqual(car.title, "Audi A4 2012 Sedan (Вінниця)")
        self.assertEqual(car.price, "10500$")
        self.assertEqual(car.year, "2012")
        self.assertIn("Седан", car.information.body_type.value)

    @patch('requests.get')
    def test_autoria_parse_car_page_success(self, mock_get):
        # Configure mock object
        mock_response = MagicMock()
        mock_response.content = AUTORIA_MOCK_HTML.encode('utf-8')
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        link = "http://auto.ria.com/test-link"
        car = autoria_parse_car_page(link)

        self.assertEqual(car.title, "Audi A4 2015 2.0 (Бензин)")
        self.assertEqual(car.price, "12 000")
        self.assertIn("Бензин", car.information.fuel_type.value)

    @patch('requests.get')
    def test_dexpens_parse_car_page_success(self, mock_get):
        # Configure mock object
        mock_response = MagicMock()
        mock_response.content = DEXPENS_MOCK_HTML.encode('utf-8')
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        link = "http://dexpens.com/test-link"
        car = dexpens_parse_car_page(link)

        self.assertEqual(car.title, "SkodaOctavia2003")
        self.assertEqual(car.price, "3500$")

    def test_extract_year_bs4_success(self):
        self.assertEqual(extract_year_bs4("Audi A4 2012 Sedan"), "2012")
        # Check that failure correctly returns None (positive check on behavior)
        self.assertIs(extract_year_bs4("Car for sale"), None)


if __name__ == '__main__':
    # Run tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)