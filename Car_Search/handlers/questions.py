
from concurrent.futures import ThreadPoolExecutor
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard
from site_parse import scrapy_parse_car
import re
from concurrent.futures import ProcessPoolExecutor
import asyncio

from car_obj import car_obj

def check_price(prices):
    if len(prices[1])==len(prices[0]) and int(prices[0][0])>int(prices[1][0]):
        return[prices[1],prices[0]]

    if int(prices[1])<int(prices[0]):
        while len(prices[0]) >= len(prices[1]):
            prices[1]=prices[1]+"0"

    return prices

def check_year(years):
    if int(years[0])>int(years[1]):
        return [years[1],years[0]]
    if int(years[0])==int(years[1]):
        return [years[0],""]
    return years
def split_car_name(car_name):
    if car_name.find('..')!=-1:
        return "",""
    parts = car_name.split(maxsplit=1)
    mark = parts[0]
    model = parts[1] if len(parts) > 1 else None
    mark=mark.strip()
    model=model.strip()
    return mark, model
def extract_year(text):
    years = re.findall(r'\b([1-9]\d{3})\b', text)
    return years[-1] if years else None
def extract_price(text):
    prices = re.findall(r'\b([1-9]\d*)\b', text)
    return prices[-1] if prices else None
def price_year(text):

    text = text.strip()

    dict_symb = [' ', '-', '.', ',', '\n']
    for delim in dict_symb:
        text = text.replace(delim, ',')

    parts = text.split(',')

    result = []

    for part in parts:

        number = re.sub(r'\D', '', part)
        if number:
            result.append(number)
    return result

def normalize_attr(s: str):
    try:
        s = s.strip()
        return s[0].upper() + s[1:].lower()
    except IndexError:
        return s
def add_list_attr(key:str,value_Str,car_char):
    try:
        value_list=value_Str.split(',')
        for i in value_list:
            try:
                if "Пропустити" not in value_list and i.find("..")==-1:
                    i=normalize_attr(i)
                    car_char.add_attr(key,i)
            except:
                None
    except:
        None

    return car_char

def count_char(car):
    if car.mark=="" or car.model=="":
        return False

    try:
        char_count=car.characteristics.check_empty()-2
        if car.price[0]=="" or car.price[1]=="":
            char_count+=1
        if car.year[0] == "" or car.year[1] == "":
            char_count += 1
    except: char_count=0

    if char_count>=3:
        return False

    return True


router = Router()  # [1]

other = "Інше"
skip="Пропустити"
available_salesmans = ["Компанія", "Автодилер","Власник", other,skip]
available_transmissions = ["Автомат", "Механіка","Типтронік","Варіатор","Робот", other,skip]
available_fuel_types = ["Дизель", "Бензин", "Газ","Електро","Водень","Гібрид", other,skip]
available_drive_types = ["Передній", "Задній","Повний","Ланцюг","Кардан", other,skip]
available_body_types = ["Купе", "Універсал","Седан","Позашляховик","Хетчбек", other,skip]
available_colors = ["Чорний", "Синій", "Білий","Коричневий","Зелений ","Сірий","Помаранчевий","Фіолетовий","Червоний","Жовтий", other,skip]


class UserState(StatesGroup):
    choosing_salesman = State()
    choosing_transmission = State()
    choosing_fuel_type = State()
    input_engine_capacity = State()
    choosing_drive_type = State()
    choosing_body_type = State()
    choosing_color = State()
    input_mileage = State()
    input_title = State()
    input_years=State()
    input_price=State()
    input_description=State()
    search_car = State()
    searched_car_list=State()
    curr_urls=State()

@router.message(Command("start"))
async def hello(message: Message):
    await message.answer(
        text="Привіт, я бот, що допоможе тобі знайти оптимальну пропозицію авто. Пиши дані коректно щоб отримати задовільну відповідь, Для початку напиши /set \n Щоб пропустити вибір характеристики напишіть '...'",
    )

@router.message(Command("set"))
async def start_get_info(message: Message, state: FSMContext):
    await message.answer(
        text="Напишіть марку та модель машини через пробіл:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.input_title)

@router.message(UserState.input_title)
async def title_choosed(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(
        text="Напишіть ціновий діапазон у доларах через дефіс:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.input_price)

@router.message(UserState.input_price)
async def price_choosed(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer(
        text="Напишіть діапазон років через дефіс:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.input_years)

@router.message(UserState.input_years)
async def years_choosed(message: Message, state: FSMContext):
    await state.update_data(years=message.text)
    await message.answer(
        text="Оголошення від:",
        reply_markup=make_row_keyboard(available_salesmans)
    )
    await state.set_state(UserState.choosing_salesman)

@router.message(UserState.choosing_salesman)
async def salesman_choosed(message: Message, state: FSMContext):


    if message.text == other:
        return await message.answer(
            text="Введіть продавця самостійно (якщо більше одного варіанту - введіть через кому):",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.update_data(salesman=message.text)
    await message.answer(
        text="Коробка передач:",
        reply_markup=make_row_keyboard(available_transmissions)
    )
    await state.set_state(UserState.choosing_transmission)

@router.message(UserState.choosing_transmission)
async def transmission_choosed(message: Message, state: FSMContext):
    if message.text == other:
        return await message.answer(
            text="Введіть коробку передач самостійно (якщо більше одного варіанту - введіть через кому):",
            reply_markup=ReplyKeyboardRemove()
        )

    await state.update_data(transmission=message.text)
    await message.answer(
        text="Тип палива:",
        reply_markup=make_row_keyboard(available_fuel_types)
    )
    await state.set_state(UserState.choosing_fuel_type)

@router.message(UserState.choosing_fuel_type)
async def fuel_type_choosed(message: Message, state: FSMContext):
    if message.text == other:
        return await message.answer(
            text="Введіть тип палива самостійно (якщо більше одного варіанту - введіть через кому):",
            reply_markup=ReplyKeyboardRemove()
        )

    await state.update_data(fuel_type=message.text)
    await message.answer(
        text="Об'єм двигуна(л.):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.input_engine_capacity)

@router.message(UserState.input_engine_capacity)
async def engine_capacity_choosed(message: Message, state: FSMContext):
    await state.update_data(engine_capacity=message.text)
    await message.answer(
        text="Тип приводу:",
        reply_markup=make_row_keyboard(available_drive_types)
    )
    await state.set_state(UserState.choosing_drive_type)

@router.message(UserState.choosing_drive_type)
async def drive_type_choosed(message: Message, state: FSMContext):
    if message.text == other:
        return await message.answer(
            text="Введіть тип приводу самостійно (якщо більше одного варіанту - введіть через кому):",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.update_data(drive_type=message.text)
    await message.answer(
        text="Тип кузова:",
        reply_markup=make_row_keyboard(available_body_types)
    )
    await state.set_state(UserState.choosing_body_type)

@router.message(UserState.choosing_body_type)
async def body_type_choosed(message: Message, state: FSMContext):
    if message.text == other:
        return await message.answer(
            text="Введіть тип кузова самостійно (якщо більше одного варіанту - введіть через кому):",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.update_data(body_type=message.text)
    await message.answer(
        text="Колір:",
        reply_markup=make_row_keyboard(available_colors)
    )
    await state.set_state(UserState.choosing_color)

@router.message(UserState.choosing_color)
async def color_choosed(message: Message, state: FSMContext):
    if message.text == other:
        return await message.answer(
            text="Введіть колір самостійно (якщо більше одного варіанту - введіть через кому):",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.update_data(color=message.text)
    await message.answer(
        text="Пробіг (тис.км):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.input_mileage)

@router.message(UserState.input_mileage)
async def location_choosed(message: Message, state: FSMContext):
    await state.update_data(mileage=message.text)
    await message.answer(
        text="Опис:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.input_description)

@router.message(UserState.input_description)
async def description_choosed(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()


    try:

        car_char = car_obj.Car_Characteristics()
        car_char=add_list_attr('Продавець', data["salesman"],car_char)
        car_char=add_list_attr('Коробка', data["transmission"],car_char)
        car_char=add_list_attr('Паливо', data["fuel_type"],car_char)
        car_char=add_list_attr('Двигун', data["engine_capacity"],car_char)
        car_char=add_list_attr('Привід', data["drive_type"],car_char)
        car_char=add_list_attr('Кузов', data["body_type"],car_char)
        car_char=add_list_attr('Колір', data["color"],car_char)
        car_char=add_list_attr('Пробіг', data["mileage"],car_char)
        car_char.display_all_characteristics()
        title = data["title"]
        try:
            mark,model=split_car_name(title)
        except:
            mark=""
            model=""



        try:
            year = data["years"]
            years=[extract_year(price_year(year)[0]),extract_year(price_year(year)[1])]
            years=check_year(years)
        except:
            years=[]

        try:
            price = data["price"]
            prices=[extract_price(price_year(price)[0]),extract_price(price_year(price)[1])]
            prices=check_price(prices)
        except:
            prices=[]




        car = car_obj.Car(mark,model,prices,years,car_char,data["description"])
        if count_char(car)==True:
            await state.update_data(search_car=car)
            message_text = f'''
            Назва: <b>{mark+' '+model}</b>
            Ціна: <b>{'від '+ prices[0]+'$ до '+prices[1]+'$'}</b>
            Рік випуску: <b>{'від '+ years[0]+'р.в до '+years[1]+'р.в'}</b>
            
            Оголошення від: <b>{data["salesman"]}</b>
            Коробка передач: <b>{data["transmission"]}</b>
            Тип палива: <b>{data["fuel_type"]}</b>
            Привід: <b>{data["drive_type"]}</b>
            Двигун: <b>{data["engine_capacity"]}</b>
            Тип кузова: <b>{data["body_type"]}</b>
            Колір: <b>{data["color"]}</b>
            Пробіг: <b>{data["mileage"]}</b>
            Опис: <b>{data["description"]}</b>
            
            Якщо інформація НЕ ВІРНА почніть спочатку: /set
            
            Якщо інформація ВІРНА почніть пошук: /search
            '''

        if count_char(car) == False:
            message_text = f'''Замало даних, почніть спочатку: /set'''


    except Exception as e:
        print("Помилка:", e)
        message_text = f'''
                Щось пішло не так або дані були введені некоректно(((
                Щоб почати щераз напишіть:/set
                '''


    await message.answer(
        text=message_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="html"
    )

    await state.set_state(UserState.search_car)


@router.message(Command("search"),UserState.search_car)
async def searching(message: Message,state: FSMContext):
    data = await state.get_data()
    await message.answer(text="Шукаємо...")
    try:

        car=data["search_car"]
        executor = ProcessPoolExecutor()
        future = executor.submit(scrapy_parse_car.start_parse_car_site, car)
        list_car,curr_urls = await asyncio.get_event_loop().run_in_executor(None, future.result)
        if list_car:
            links=f''''''
            message_text = f'''ЗНАЙШЛИ!!! '''

            if len(list_car)<=10:
                for i in list_car:
                    car_text= i.title + ' ' + i.price + '\n'
                    links += f'''<a href="{i.link}">{car_text}</a>'''
                message_text=message_text+ '\n'  + links + '''\n '''
                message_text = message_text + "Почати ще раз: /set"

            else:
                for i in range(0,10):
                    car_text = list_car[i].title + ' ' + list_car[i].price + '\n'
                    links += f'''<a href="{list_car[i].link}">{car_text}</a>'''
                list_car=list_car[10:]
                message_text = message_text + '\n' + links + '\n'+'''Щоб подивить більше: /more'''

        if not list_car:
            message_text = f'''Нічого не знайдено! '''
            message_text = message_text + "Варто ввести більш реалістичні дані"
            message_text = message_text + "Почати ще раз: /set"

        print(curr_urls)

        await state.update_data(searched_car_list=list_car)
        await state.set_state(UserState.searched_car_list)
        await state.update_data(curr_urls=curr_urls)
        await state.set_state(UserState.curr_urls)

    except Exception as e:
        print("Помилка:", e)
        list_car=None
        message_text = f'''
        Щось пішло не так(((
        Щоб почати щераз напишіть: /set
        '''



    await message.answer(
        text=message_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="html",
        disable_web_page_preview=True

    )




@router.message(Command("more"))
async def more(message: Message,state: FSMContext):
    data = await state.get_data()
    list_car=data["searched_car_list"]
    curr_urls = data["curr_urls"]
    message_text = f'''Інші варіанти:'''
    links = ""
    if len(list_car) <= 10:
        for i in list_car:
            car_text = i.title + ' ' + i.price + '\n'
            links += f'''<a href="{i.link}">{car_text}</a>'''
        message_text = message_text + '\n' + links + '''\n '''
        message_text = message_text + "Почати ще раз: /set"

        if curr_urls[0] != '' or curr_urls[1] != '':
            message_text = message_text + '\n' +"Продовжити пошук: /continue"
    else:
        for i in range(0, 10):
            car_text = list_car[i].title + ' ' + list_car[i].price + '\n'
            links += f'''<a href="{list_car[i].link}">{car_text}</a>'''
        list_car = list_car[10:]
        message_text = message_text + '\n' + links + '\n' + '''Щоб подивить більше: /more '''
        message_text = message_text + '\n' + "Почати ще раз: /set"

    await message.answer(
        text=message_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="html",
        disable_web_page_preview=True
    )
    await state.update_data(searched_car_list=list_car)
    await state.set_state(UserState.searched_car_list)


@router.message(Command("continue"))
async def cont_searching(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text="Шукаємо...")
    try:

        car = data["search_car"]
        curr_urls=data["curr_urls"]
        executor = ProcessPoolExecutor()
        future = executor.submit(scrapy_parse_car.continue_parse_car_site, car,curr_urls)
        list_car, curr_urls = await asyncio.get_event_loop().run_in_executor(None, future.result)
        if list_car:
            links = f''''''
            message_text = f'''ЗНАЙШЛИ!!! '''

            if len(list_car) <= 10:
                for i in list_car:
                    car_text = i.title + ' ' + i.price + '\n'
                    links += f'''<a href="{i.link}">{car_text}</a>'''
                message_text = message_text + '\n' + links + '''\n '''
                message_text = message_text + "Почати ще раз: /set"

            else:
                for i in range(0, 10):
                    car_text = list_car[i].title + ' ' + list_car[i].price + '\n'
                    links += f'''<a href="{list_car[i].link}">{car_text}</a>'''
                list_car = list_car[10:]
                message_text = message_text + '\n' + links + '\n' + '''Щоб подивить більше: /more'''

        if not list_car:
            message_text = f'''Нічого не знайдено! '''
            message_text = message_text + "Почати ще раз: /set"

        print(curr_urls)

        await state.update_data(searched_car_list=list_car)
        await state.set_state(UserState.searched_car_list)
        await state.update_data(curr_urls=curr_urls)
        await state.set_state(UserState.curr_urls)

    except Exception as e:
        print("Помилка:", e)
        list_car = None
        message_text = f'''
        Щось пішло не так(((
        Щоб почати щераз напишіть: /set
        '''

    await message.answer(
        text=message_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="html",
        disable_web_page_preview=True

    )







@router.message(Command("test2"))
async def test(message: Message):
    await message.answer(text="Погнали тест 2")

    char = car_obj.Car_Characteristics()
    # char.add_attr("Коробка", "Механіка")
    # char.add_attr("Двигун", "2")
    # char.add_attr("Кузов", "Седан")
    # char.add_attr("Колір", "Чорний")
    # char.add_attr("Пробіг", "300")
    # char.add_attr("Привід", "Передній")
    car_ = car_obj.Car("Audi", "A4", ["3000", "7000"], ["2000", "2010"], char, "Топ")

    executor = ProcessPoolExecutor()
    future = executor.submit(scrapy_parse_car.start_parse_car_site, car_)
    list_car, curr_link = await asyncio.get_event_loop().run_in_executor(None, future.result)

    text = ""
    for car in list_car:
        text += car.link + '\n'


    text+='\n'+str(len(list_car))
    await message.answer(text=text,disable_web_page_preview=True)

    executor = ProcessPoolExecutor()
    future = executor.submit(scrapy_parse_car.continue_parse_car_site, car_,curr_link)
    list_car, curr_link = await asyncio.get_event_loop().run_in_executor(None, future.result)

    text = ""
    for car in list_car:
        text += car.link + '\n'

    text += '\n' + str(len(list_car))
    await message.answer(text=text, disable_web_page_preview=True)


