import logging
from bs4 import BeautifulSoup
import requests
from car_obj import car_obj

# logging.basicConfig(
#     level='INFO',
#     format='[%(levelname)-5s] %(asctime)s\t-\t%(message)s',
#     datefmt='%d/%m/%Y %I:%M:%S %p'
# )


def automoto_parse_car_page(link)->car_obj.car_obj:
    # ### unique extractor
    url = link
    response = requests.get(url)
    print(response.status_code)
    res = BeautifulSoup(response.content, features="html.parser")


    ## Title
    try:
        title = res.find('h1', class_='main-card-name').text.strip().replace("\xa0", " ")
    except:
        title = None

    ## description
    try:
        description = res.select('.pb-0 .px-md-0')[0].text.strip()
    except:
        description = None
    try:
        content1=res.find('div', class_='pb-0').find('div', class_='px-md-0').find_all('p')
        for i in content1:
            description+="\n"+(i.text.strip().replace("\xa0", " "))
    except:
        description=None


    ## Price
    try:
        price = res.find('div', attrs={'class': 'price-item'}).text.strip().replace(" ","")
    except:
        price = None

#information
    try:
        car_character=car_obj.Car_Characteristics()
        information=""
        info_table=res.find('div',class_='py-md-0').find_all('tr')
        for i in info_table:
            td_tag=i.find_all('td')
            information+=td_tag[0].text.strip()+" "+td_tag[1].text.strip()+'\n'
            car_character.add_attr(td_tag[0].text.strip(),td_tag[1].text.strip())

    except:
        information = None


    car = car_obj.car_obj(str(title),str(price),car_character,str(description),str(link))

    return car

def avtobazar_parse_car_page(link)->car_obj.car_obj:
    # ### unique extractor
    url = link
    response = requests.get(url)
    print(response.status_code)
    res = BeautifulSoup(response.content,'html.parser')


    ## Title
    try:
        title = res.find('div',class_='_32c5u').text.strip()
    except:
        title = None

    ## Price
    try:
        price = res.find('div',class_='_2izCF').text.strip()
    except:
        try:
            price=res.find('span', attrs={'data-currency': 'usd'}).text.strip().replace('•','')
        except:
            price = None

    ## description
    try:
        description = res.find('div', class_='_1d01p').text.strip()
    except:
        description = None

    # information
    try:
        car_character = car_obj.Car_Characteristics()
        information = ""
        info_table = res.find_all('div', class_='heJ1W')
        for i in info_table:
            key=i.find('span',class_='_1hnlw').text.strip()
            value=i.find('span',class_='_27p5n').text.strip()
            if key=='Пробіг' and value=='новий':
                value='0'
            if key=='Двигун':
                try:
                    l=str(value).split('/')
                    car_character.add_attr('Двигун',l[1].strip())
                    car_character.add_attr('Паливо',l[0].strip())

                except:car_character.add_attr(key,value)
            else:
                car_character.add_attr(key,value)



    except:
        information = None

    car = car_obj.car_obj(str(title), str(price), car_character, str(description), str(link))

    return car

def autoria_parse_car_page(link)->car_obj.car_obj:
    # ### unique extractor
    url = link
    response = requests.get(url)
    print(response.status_code)
    res = BeautifulSoup(response.content,'html.parser')


    ## Title
    try:
        title = res.find('h1',class_='head').text.strip()
    except:
        title = None

    ## Price
    try:
        price = res.find('div', class_='price_value').find('strong').text.strip()
    except:
        price = None

    ## description
    try:
        description = res.find('div', class_='full-description').text.strip()
    except:
        description = None

    # information
    try:
        car_character = car_obj.Car_Characteristics()
        charsc = res.select('#details dd:nth-child(1)')[0].text.strip()
        charsc=charsc.split('•')
        car_character.add_attr('Тип кузова',charsc[0])
        try:
            car_character.add_attr('Місць в салоні', charsc[2])
        except:
            car_character.add_attr('Місць в салоні', charsc[1])

        info_table = res.select('.description-car .technical-info dd:not(.show-line)')
        for i in info_table:
            try:
                key=i.find('span',class_='label').text.strip()
                value=i.find('span',class_='argument').text.strip()
            except:
                continue
            if key=='Двигун':
                try:
                    l=str(value).split('•')
                    car_character.add_attr('Двигун',l[0].strip())
                    car_character.add_attr('Паливо',l[1].strip())

                except:car_character.add_attr(key,value)
            else:
                car_character.add_attr(key,value)

    except:
         None

    car = car_obj.car_obj(str(title), str(price), car_character, str(description), str(link))

    return car


# car=autoria_parse_car_page('https://auto.ria.com/uk/auto_skoda_kodiaq_36549938.html')
# print(car.title,'\n')
# print(car.price,'\n')
# print(car.description,'\n')
# car.information.display_all_characteristics()