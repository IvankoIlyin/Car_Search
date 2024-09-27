import time
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from car_obj import car_obj

def time_sllep():
    time.sleep(0.5)

def selenium_parse_automoto(car:car_obj.Car):

    options=webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    link='https://automoto.ua/uk/'
    driver.get(link)
    time_sllep()
    #mark
    try:
        if car.mark!="":
            driver.find_element(By.CSS_SELECTOR,'.choices .choices__inner').click()
            time_sllep()
            driver.find_element(By.CSS_SELECTOR,'.choices__input.choices__input--cloned[aria-label="Марка"]').send_keys(car.mark)
            time_sllep()
            driver.find_element(By.CSS_SELECTOR,'.choices__list .choices__item:first-child.is-highlighted').click()
            time_sllep()
    except:
        None
    #model
    try:
        if car.model != "":
            driver.find_element(By.CSS_SELECTOR,'.choices_model+ .choices__list--single .choices__item--selectable').click()
            time_sllep()
            driver.find_element(By.CSS_SELECTOR,'.choices__input.choices__input--cloned[aria-label="Модель"]').send_keys(car.model)
            time_sllep()
            driver.find_element(By.CSS_SELECTOR,'.choices__list .choices__item:first-child.is-highlighted').click()
            time_sllep()
    except:
        None
    # Price
    try:
        if car.price[0] != "":
            price = driver.find_element(By.CSS_SELECTOR, 'input[name="price[from]"]')
            price.send_keys(car.price[0])
            time_sllep()
        if car.year[0] != "":
            driver.find_element(By.CSS_SELECTOR, 'select[name="year[from]"] option[value="' + car.year[0] + '"]').click()
            time_sllep()
    except:None
    # Year
    try:
        if car.price[1] != "":
            price = driver.find_element(By.CSS_SELECTOR, 'input[name="price[to]"]')
            price.send_keys(car.price[1])
            time_sllep()
        if car.year[1] != "":
            driver.find_element(By.CSS_SELECTOR, 'select[name="year[to]"] option[value="' + car.year[1] + '"]').click()
            time_sllep()
    except:None




    #Search
    driver.find_element(By.CSS_SELECTOR,".btn-main.btn-block").click()
    time_sllep()

    #FILTER


    #body type
    try:
        if car.characteristics.body_type.value:
            more=driver.find_element(By.CSS_SELECTOR,'#collapseBodyType+ .collapsed')
            driver.execute_script("arguments[0].scrollIntoView(true);", more)
            time_sllep()
            more.click()
            for i in car.characteristics.body_type.value:
                body_type=driver.find_element(By.XPATH,'.//div[contains(concat(" ",normalize-space(@class)," ")," custom-control ")][contains(normalize-space(),"'+i+'")]')
                driver.execute_script("arguments[0].scrollIntoView(true);", body_type)
                time_sllep()
                body_type.click()

    except:None


    #transmission
    try:
        if car.characteristics.transmission.value:
            more = driver.find_element(By.CSS_SELECTOR, '#collapseTransmission+ .collapsed')
            driver.execute_script("arguments[0].scrollIntoView(true);", more)
            time_sllep()
            more.click()
            for i in car.characteristics.transmission.value:
                transmission=driver.find_element(By.XPATH,
                                    './/div[contains(concat(" ",normalize-space(@class)," ")," custom-control ")][contains(normalize-space(),"' + i + '")]')
                driver.execute_script("arguments[0].scrollIntoView(true);", transmission)
                time_sllep()
                transmission.click()
    except:None



    # engine_capacity
    try:
        if car.characteristics.engine_capacity.value:
            for i in car.characteristics.engine_capacity.value:
                engine_capacity = driver.find_element(By.CSS_SELECTOR, 'input[name="engine_volume[to]')
                driver.execute_script("arguments[0].scrollIntoView(true);", engine_capacity)
                time_sllep()
                engine_capacity.send_keys(str(i))
    except:None


    #drive_type
    try:
        if car.characteristics.drive_type.value:
            for i in car.characteristics.drive_type.value:
                drive_type=driver.find_element(By.XPATH,
                                    './/div[contains(concat(" ",normalize-space(@class)," ")," custom-control ")][contains(normalize-space(),"' + i + '")]')
                driver.execute_script("arguments[0].scrollIntoView(true);", drive_type)
                time_sllep()
                drive_type.click()
    except:None


    #mileage
    try:
        if car.characteristics.mileage.value:
            for i in car.characteristics.mileage.value:
                mileage=driver.find_element(By.CSS_SELECTOR,'input[name="mileage[to]"]')
                driver.execute_script("arguments[0].scrollIntoView(true);", mileage)
                time_sllep()
                mileage.send_keys(str(i))
    except: None


    # color
    try:
        if car.characteristics.color.value:
            for i in car.characteristics.color.value:
                drive_type = driver.find_element(By.XPATH,
                                                 './/div[contains(concat(" ",normalize-space(@class)," ")," custom-control ")][contains(normalize-space(),"' + i + '")]')
                driver.execute_script("arguments[0].scrollIntoView(true);", drive_type)
                time_sllep()
                drive_type.click()
                time_sllep()
    except:None

    try:
        driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-main[type="submit"]').click()
        time_sllep()
    except:
        None


    link=driver.current_url
    driver.close()

    return link
def selenium_parse_autoria(car:car_obj.Car):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument('--disable-gpu')
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    link='https://auto.ria.com/uk/'
    driver.get(link)
    time_sllep()
    try:
        driver.find_element(By.CSS_SELECTOR,'.c-notifier-container.c-notifier-start label.js-close[onclick="setAllGdpr()"]').click()
    except:
        None

    # mark
    try:
        if car.mark!="":
            driver.find_element(By.CSS_SELECTOR, '#brandTooltipBrandAutocomplete-brand').click()
            time_sllep()
            driver.find_element(By.CSS_SELECTOR, '#brandTooltipBrandAutocomplete-brand input[placeholder="Пошук..."]').send_keys(
                car.mark)
            time_sllep()
            driver.find_element(By.CSS_SELECTOR, '#brandTooltipBrandAutocomplete-brand ul.unstyle.scrollbar.autocomplete-select li.list-item:first-child').click()
            time_sllep()
    except:
        None

    # model
    try:
        if car.model != "":
            driver.find_element(By.CSS_SELECTOR,
                                    '#brandTooltipBrandAutocomplete-model').click()
            time_sllep()
            driver.find_element(By.CSS_SELECTOR,
                                    '#brandTooltipBrandAutocomplete-model input[placeholder="Пошук..."]').send_keys(car.model)
            time_sllep()
            driver.find_element(By.CSS_SELECTOR, '#brandTooltipBrandAutocomplete-model ul.unstyle.scrollbar.autocomplete-select li.list-item:first-child').click()
            time_sllep()
    except:
        None

     # Year
    try:
            driver.find_element(By.CSS_SELECTOR, '.e-year ._grey').click()
            if car.year[0]!="":
                time_sllep()
                driver.find_element(By.CSS_SELECTOR, '#yearFrom').click()
                time_sllep()
                driver.find_element(By.CSS_SELECTOR, 'select#yearFrom option[value="' + car.year[0] + '"]').click()
                time_sllep()
            else:None
            if car.year[1] != "":
                driver.find_element(By.CSS_SELECTOR, '#yearTo').click()
                time_sllep()
                driver.find_element(By.CSS_SELECTOR, 'select#yearTo option[value="' + car.year[1] + '"]').click()
                time_sllep()
            else:
                None
            clickable = driver.find_element(By.CSS_SELECTOR, '.popup-body')
            ActionChains(driver) \
                .click(clickable) \
                .perform()
            time_sllep()
            driver.find_element(By.CSS_SELECTOR, 'label.fold[for="forYear"]').click()
            time_sllep()


    except:
            None


    # Price
    try:
        if car.price[0] != "":
            driver.find_element(By.CSS_SELECTOR, '.e-cost ._grey').click()
            time_sllep()
            driver.find_element(By.CSS_SELECTOR, 'input#priceFrom').send_keys(car.price[0])
            time_sllep()
        if car.price[1] != "":
            driver.find_element(By.CSS_SELECTOR, 'input#priceTo').send_keys(car.price[1])
            time_sllep()
            driver.find_element(By.CSS_SELECTOR, 'label.fold[for="forPrice"]').click()
            time_sllep()
    except:
        None



    # Search
    driver.find_element(By.CSS_SELECTOR, ".full").click()
    time.sleep(3)

    # FILTER

    # body type
    try:
        if car.characteristics.body_type.value:
            driver.execute_script("arguments[0].scrollIntoView(true);",
                                  driver.find_element(By.CSS_SELECTOR, '#bodyBlock .bold'))

            time.sleep(1)


            clickable = driver.find_element(By.CSS_SELECTOR, '#bodyBlock .open')
            ActionChains(driver) \
                .click(clickable) \
                .perform()

            time.sleep(2)
            for i in car.characteristics.body_type.value:
                body_type = driver.find_element(By.XPATH,
                                                './/*[contains(concat(" ",normalize-space(@class)," ")," item-rows ")][@title="Тип кузова"]//label[contains(normalize-space(),"'+i+'")]')
                driver.execute_script("arguments[0].scrollIntoView(true);", body_type)
                time.sleep(1)
                body_type.click()
    except:
        None



    # mileage
    try:
        if car.characteristics.mileage.value:
            for i in car.characteristics.mileage.value:
                engine_capacity = driver.find_element(By.CSS_SELECTOR, 'input[name="mileage.lte')
                driver.execute_script("arguments[0].scrollIntoView(true);", engine_capacity)
                time_sllep()
                engine_capacity.send_keys(str(i))
    except:
        None



    # transmission
    try:
        if car.characteristics.transmission.value:
            driver.execute_script("arguments[0].scrollIntoView(true);",
                                  driver.find_element(By.CSS_SELECTOR, '#gearboxBlock .bold'))

            time_sllep()

            clickable = driver.find_element(By.CSS_SELECTOR, '#gearboxBlock .open')
            ActionChains(driver) \
                .click(clickable) \
                .perform()

            time_sllep()
            for i in car.characteristics.transmission.value:
                body_type = driver.find_element(By.XPATH,
                                                './/*[contains(concat(" ",normalize-space(@class)," ")," item-rows ")][@title="Коробка передач"]//label[contains(normalize-space(),"'+i+'")]')
                time_sllep()
                driver.execute_script("arguments[0].scrollIntoView(true);", body_type)
                time_sllep()
                body_type.click()
                time_sllep()
    except:
        None




    # engine_capacity
    try:
        if car.characteristics.engine_capacity.value:
            for i in car.characteristics.engine_capacity.value:
                engine_capacity = driver.find_element(By.CSS_SELECTOR, 'input[name="engine.lte')
                driver.execute_script("arguments[0].scrollIntoView(true);", engine_capacity)
                time_sllep()
                engine_capacity.send_keys(str(i))
    except:
        None





    # drive_type
    try:
        if car.characteristics.drive_type.value:
            driver.execute_script("arguments[0].scrollIntoView(true);",
                                  driver.find_element(By.CSS_SELECTOR, '#driveBlock .bold'))

            time_sllep()
            for i in car.characteristics.drive_type.value:
                body_type = driver.find_element(By.CSS_SELECTOR,
                                                '.item-rows[title="Тип приводу"] label[title="' + i + '"]')
                driver.execute_script("arguments[0].scrollIntoView(true);", body_type)
                time_sllep()
                body_type.click()
    except:
        None

    try:
        driver.find_element(By.CSS_SELECTOR, '#floatingSearchButton').click()
        time_sllep()
    except:
        None

    link = driver.current_url
    driver.close()

    return link
def selenium_parse_dexpens(car:car_obj.Car):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    link='https://www.dexpens.com/Automarket'
    driver.get(link)
    time.sleep(3)

    # mark
    try:
        driver.find_element(By.CSS_SELECTOR, '#select2-Make_0-container').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.select2-search__field').send_keys(
            car.mark)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.select2-results__option--highlighted').click()
        time.sleep(1)
    except:
        None

    # model
    try:
        driver.find_element(By.CSS_SELECTOR, '#select2-Model_0-container').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.select2-search__field').send_keys(car.model)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.select2-results__option--highlighted').click()
        time.sleep(1)
    except:
        None

    # Year
    try:
        driver.find_element(By.CSS_SELECTOR, '#select2-FromYear_0-container').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.select2-search__field').send_keys(car.year[0])
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.select2-results__option--highlighted').click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, '#select2-ToYear_0-container').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.select2-search__field').send_keys(car.year[1])
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.select2-results__option--highlighted').click()
        time.sleep(1)
    except:
        None

    # Price
    try:
        driver.find_element(By.CSS_SELECTOR, '#PriceFrom').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#PriceFrom').send_keys(car.price[0])
        time.sleep(1)


        driver.find_element(By.CSS_SELECTOR, '#PriceTo').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#PriceTo').send_keys(car.price[1])
        time.sleep(1)
    except:
        None


    # try:
    #     driver.find_element(By.CSS_SELECTOR, '#filterSearch').click()
    #     time.sleep(1)
    # except:
    #     None
    #
    # try:
    #     driver.find_element(By.CSS_SELECTOR, '#filterCarSelling').click()
    #     time.sleep(1)
    # except:
    #     None

    #Filter
    # try:
    #     driver.find_element(By.CSS_SELECTOR, '#advancedSearch').click()
    #     time.sleep(1)
    # except:
    #     None

    #mileage
    # try:
    #     mileage=driver.find_element(By.CSS_SELECTOR,'#MileageTo')
    #     driver.execute_script("arguments[0].scrollIntoView(true);",mileage)
    #     time.sleep(1)
    #     ActionChains(driver) \
    #         .click(mileage) \
    #         .perform()
    #     time.sleep(5)
    # except:
    #     None

    #transmission
    # try:
    #     transmission=driver.find_element(By.CSS_SELECTOR,'#Transmission_chosen')
    #     driver.execute_script("arguments[0].scrollIntoView(true);",transmission)
    #     time.sleep(1)
    #     cl=driver.find_element(By.CSS_SELECTOR,'#Transmission_chosen span')
    #     ActionChains(driver) \
    #         .click(cl) \
    #         .perform()
    #     time.sleep(5)
    # except:
    #     None



    try:
        driver.find_element(By.CSS_SELECTOR, '#filterSearch').click()
        time.sleep(1)
    except:
        None
    link = driver.current_url
    driver.close()

    return link


char = car_obj.Car_Characteristics()
char.add_attr("Коробка", "Механіка")
char.add_attr("Двигун", "2")
char.add_attr("Кузов", "Седан")
char.add_attr("Кузов", "Купе")
char.add_attr("Колір", "Чорний")
char.add_attr("Колір", "Білий")
char.add_attr("Пробіг", "300")
char.add_attr("Привід", "Передній")
char.add_attr("Привід", "Задній")
char.add_attr("Привід", "Ланцюг")
car = car_obj.Car("Audi", "A4", ["3000", "5000"], ["2000", "2010"], char, "Топ")
car.characteristics.display_all_characteristics()

print(selenium_parse_automoto(car))