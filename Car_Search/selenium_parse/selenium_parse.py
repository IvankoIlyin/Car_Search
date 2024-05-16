import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from car_obj import car_obj



def selenium_parse_automoto(car:car_obj.Car):

    driver = webdriver.Chrome()
    link='https://automoto.ua/uk/'
    driver.get(link)
    time.sleep(1)
    #mark
    try:
        driver.find_element(By.CSS_SELECTOR,'.choices .choices__inner').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,'.choices__input.choices__input--cloned[aria-label="Марка"]').send_keys(car.mark)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,'.choices__list .choices__item:first-child.is-highlighted').click()
        time.sleep(1)
    except:
        None
    #model
    try:
        driver.find_element(By.CSS_SELECTOR,'.choices_model+ .choices__list--single .choices__item--selectable').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,'.choices__input.choices__input--cloned[aria-label="Модель"]').send_keys(car.model)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,'.choices__list .choices__item:first-child.is-highlighted').click()
        time.sleep(1)
    except:
        None
    # Price
    try:
        price = driver.find_element(By.CSS_SELECTOR, 'input[name="price[from]"]')
        price.send_keys(car.price[0])
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'select[name="year[from]"] option[value="' + car.year[0] + '"]').click()
        time.sleep(1)
    except:None
    # Year
    try:
        price = driver.find_element(By.CSS_SELECTOR, 'input[name="price[to]"]')
        price.send_keys(car.price[1])
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'select[name="year[to]"] option[value="' + car.year[1] + '"]').click()
        time.sleep(1)
    except:None




    #Search
    driver.find_element(By.CSS_SELECTOR,".btn-main.btn-block").click()
    time.sleep(1)

    #FILTER


    #body type
    try:
        more=driver.find_element(By.CSS_SELECTOR,'#collapseBodyType+ .collapsed')
        driver.execute_script("arguments[0].scrollIntoView(true);", more)
        time.sleep(1)
        more.click()
        for i in car.characteristics.body_type.value:
            body_type=driver.find_element(By.XPATH,'.//div[contains(concat(" ",normalize-space(@class)," ")," custom-control ")][contains(normalize-space(),"'+i+'")]')
            driver.execute_script("arguments[0].scrollIntoView(true);", body_type)
            time.sleep(1)
            body_type.click()
    except:None
    #transmission
    try:
        more = driver.find_element(By.CSS_SELECTOR, '#collapseTransmission+ .collapsed')
        driver.execute_script("arguments[0].scrollIntoView(true);", more)
        time.sleep(1)
        more.click()
        for i in car.characteristics.transmission.value:
            transmission=driver.find_element(By.XPATH,
                                './/div[contains(concat(" ",normalize-space(@class)," ")," custom-control ")][contains(normalize-space(),"' + i + '")]')
            driver.execute_script("arguments[0].scrollIntoView(true);", transmission)
            time.sleep(1)
            transmission.click()
    except:None
    # engine_capacity
    try:
        for i in car.characteristics.engine_capacity.value:
            engine_capacity = driver.find_element(By.CSS_SELECTOR, 'input[name="engine_volume[to]')
            driver.execute_script("arguments[0].scrollIntoView(true);", engine_capacity)
            time.sleep(1)
            engine_capacity.send_keys(str(i))
    except:None
    #drive_type
    try:
        for i in car.characteristics.drive_type.value:
            drive_type=driver.find_element(By.XPATH,
                                './/div[contains(concat(" ",normalize-space(@class)," ")," custom-control ")][contains(normalize-space(),"' + i + '")]')
            driver.execute_script("arguments[0].scrollIntoView(true);", drive_type)
            time.sleep(1)
            drive_type.click()
    except:None


    #mileage
    try:
        for i in car.characteristics.mileage.value:
            mileage=driver.find_element(By.CSS_SELECTOR,'input[name="mileage[to]"]')
            driver.execute_script("arguments[0].scrollIntoView(true);", mileage)
            time.sleep(1)
            mileage.send_keys(str(i))
    except: None


    # color
    try:
        for i in car.characteristics.color.value:
            drive_type = driver.find_element(By.XPATH,
                                             './/div[contains(concat(" ",normalize-space(@class)," ")," custom-control ")][contains(normalize-space(),"' + i + '")]')
            driver.execute_script("arguments[0].scrollIntoView(true);", drive_type)
            time.sleep(1)
            drive_type.click()
            time.sleep(1)
    except:None




    link=driver.current_url
    driver.close()

    return link

def selenium_parse_avtobazar(car:car_obj.Car):
    driver = webdriver.Chrome()
    driver.get('https://avtobazar.ua/uk/')
    time.sleep(1)
    # mark

def selenium_parse_autoria(car:car_obj.Car):
    driver = webdriver.Chrome()
    link='https://auto.ria.com/uk/'
    driver.get(link)
    time.sleep(3)

    # mark
    try:
        driver.find_element(By.CSS_SELECTOR, '#brandTooltipBrandAutocomplete-brand').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#brandTooltipBrandAutocomplete-brand input[placeholder="Пошук..."]').send_keys(
            car.mark)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#brandTooltipBrandAutocomplete-brand ul.unstyle.scrollbar.autocomplete-select li.list-item:first-child').click()
        time.sleep(1)
    except:
        None

    # model
    try:
        driver.find_element(By.CSS_SELECTOR,
                                '#brandTooltipBrandAutocomplete-model').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,
                                '#brandTooltipBrandAutocomplete-model input[placeholder="Пошук..."]').send_keys(car.model)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#brandTooltipBrandAutocomplete-model ul.unstyle.scrollbar.autocomplete-select li.list-item:first-child').click()
        time.sleep(1)
    except:
        None

     # Year
    try:
            driver.find_element(By.CSS_SELECTOR, '.e-year ._grey').click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '#yearFrom').click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, 'select#yearFrom option[value="' + car.year[0] + '"]').click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '#yearTo').click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, 'select#yearTo option[value="' + car.year[1] + '"]').click()
            time.sleep(1)
            clickable = driver.find_element(By.CSS_SELECTOR, '.popup-body')
            ActionChains(driver) \
                .click(clickable) \
                .perform()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, 'label.fold[for="forYear"]').click()
            time.sleep(1)


    except:
            None


    # Price
    try:
        driver.find_element(By.CSS_SELECTOR, '.e-cost ._grey').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input#priceFrom').send_keys(car.price[0])
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input#priceTo').send_keys(car.price[1])
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'label.fold[for="forPrice"]').click()
        time.sleep(1)
    except:
        None



    # Search
    driver.find_element(By.CSS_SELECTOR, ".full").click()
    time.sleep(1)

    # FILTER

    # body type
    try:
        #more = driver.find_element(By.CSS_SELECTOR, '#bodyBlock .bold')

        driver.execute_script("arguments[0].scrollIntoView(true);",
                              driver.find_element(By.CSS_SELECTOR, '#bodyBlock .bold'))

        time.sleep(5)

        clickable = driver.find_element(By.CSS_SELECTOR, '#bodyBlock .open')
        ActionChains(driver) \
            .click(clickable) \
            .perform()
        time.sleep(5)

        time.sleep(1)
        for i in car.characteristics.body_type.value:
            body_type = driver.find_element(By.CSS_SELECTOR,'.item-rows[title="Тип кузова"] label[title="'+i+'"]')
            driver.execute_script("arguments[0].scrollIntoView(true);", body_type)
            time.sleep(1)
            body_type.click()
    except:
        None

    link = driver.current_url
    driver.close()

    return link

car_char=car_obj.Car_Characteristics()

car_char.add_attr("Тип палива","Бензин")
car_char.add_attr("Коробка","Автомат")
car_char.add_attr("Коробка","Механіка")
car_char.add_attr("Коробка","Варіатор")
car_char.add_attr("Тип кузова","Седан")
car_char.add_attr("Тип кузова","Пікап")
car_char.add_attr("Тип кузова","Універсал")
car_char.add_attr("Тип кузова","Хетчбек")
car_char.add_attr("Тип кузова","Мінівен")
car_char.add_attr("Тип кузова","Купе")
car_char.add_attr("Тип кузова","Фургон")
car_char.add_attr("Привід","Передній")
car_char.add_attr("Колір","Чорний")
car_char.add_attr("Колір","Білий")
car_char.add_attr("Колір","Червоний")
car_char.add_attr("Пробіг","300000л")
car_char.add_attr("Двигун","1л")




car=car_obj.Car("Audi","A4",["10000$","30000$"],["2010","2020"],car_char)

print(selenium_parse_autoria(car))