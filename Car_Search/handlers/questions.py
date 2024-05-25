import asyncio
from concurrent.futures import ThreadPoolExecutor
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from car_obj import car_obj
from keyboards.simple_row import make_row_keyboard
from site_parse import scrapy_parse_car
import re

def extract_year(text):
    years = re.findall(r'\b([1-9]\d{3})\b', text)
    return years[-1] if years else None
def extract_price(text):
    prices = re.findall(r'\b([1-9]\d*)\b', text)
    return prices[-1] if prices else None

def price_year(text):
    dict_symb = [' ','-', '.', ',', '\n']
    for i in dict_symb:
        price_arr=text.split(i)
        if len(price_arr)>=2:
            return price_arr

    return None

def normalize_attr(s: str):
    try:
        s = s.strip()
        return s[0].upper() + s[1:].lower()
    except IndexError:
        return s

def add_list_attr(key:str,value_Str):
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
        print('Fuuck')


async def start_parse(search_list):
    loop=asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        data= await loop.run_in_executor(pool,scrapy_parse_car.start_parse_car_site,search_list)
    return data


car=car_obj.Car()
car_char = car_obj.Car_Characteristics()



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

@router.message(Command("start"))
async def hello(message: Message):
    await message.answer(
        text="Привіт, я бот, що допоможе тобі знайти оптимальну пропозицію авто. Пиши дані коректно щоб отримати задовільну відповідь, Для початку напиши /set \n Щоб пропустити вибір характеристики напишіть '...'",
    )



@router.message(Command("set"))
async def start_get_info(message: Message, state: FSMContext):
    car_char.clear()
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
            text="Введіть продавця самостійно(якщо більше одного варіанту - введіть через кому):",
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
            text="Введіть коробку передач самостійно(якщо більше одного варіанту - введіть через кому):",
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
            text="Введіть тип палива самостійно(якщо більше одного варіанту - введіть через кому):",
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
            text="Введіть тип приводу самостійно(якщо більше одного варіанту - введіть через кому):",
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
            text="Введіть тип кузова самостійно(якщо більше одного варіанту - введіть через кому):",
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
            text="Введіть колір самостійно(якщо більше одного варіанту - введіть через кому):",
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

        add_list_attr('Продавець', data["salesman"])
        add_list_attr('Коробка', data["transmission"])
        add_list_attr('Паливо', data["fuel_type"])
        add_list_attr('Двигун', data["engine_capacity"])
        add_list_attr('Привід', data["drive_type"])
        add_list_attr('Кузов', data["body_type"])
        add_list_attr('Колір', data["color"])
        add_list_attr('Пробіг', data["mileage"])

        car_char.display_all_characteristics()


        title = data["title"].split(' ')
        mark,model="",""
        try:
            mark=title[0]
        except:
            mark=""
        try:
            model=title[1]
        except:
            model=""



        year = data["years"].split('-')
        years=[]
        try:
            years.append(year[0])
        except:
            years.append("")
        try:
            years.append(year[1])
        except:
            years.append("")


        price = data["price"].split('-')
        prices=[]
        try:
            prices.append(price[0])
        except:
            prices.append("")
        try:
            prices.append(price[1])
        except:
            prices.append("")


        print(mark)
        print(model)
        print(prices[0])
        print(prices[1])
        print(years[0])
        print(years[1])

        car.mark=mark
        car.model=model
        car.price=prices
        car.year=years
        car.characteristics=car_char
        car.dedescription=data["description"]


        message_text = f'''
        
        Назва: <b>{data["title"]}</b>
        Ціна: <b>{data["price"]}</b>
        Роки: <b>{data["years"]}</b>
        
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
        
        Якщо інформація ВІРНА почніть спочатку: /search
        '''
    except:
        message_text = f'''
                Щось пішло не так або дані були введені некоректно(((
                
                Щоб почати щераз напишіть: /set

                '''


    await message.answer(
        text=message_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="html"
    )
    await state.clear()

@router.message(Command("search"))
async def searching(message: Message):

    message_text = f'''
        Шукаємо авто...
        '''
    await message.answer(
        text=message_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="html"
    )

    try:
        # list_car = scrapy_parse_car.start_parse_car_site(car)
        list_car=await start_parse(car)
        links=""
        message_text = f'''ЗНАЙШЛИ!!! '''

        if len(list_car)<=10:
            for i in list_car:
                links+=i.link+'\n'+'\n'
            message_text+=message_text+ '\n'  + links + '''\n '''
        else:
            for i in range(0,10):
                links+=list_car[i].link+'\n'+'\n'
            list_car=list_car[10:]
            message_text += message_text + '\n' + links + '\n'+'''Щоб подивить більше: /more'''

    except:
        message_text = f'''
        Щось пішло не так(((
        
        Щоб почати щераз напишіть: /set

        '''

    await message.answer(
        text=message_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="html"
    )

# @router.message(Command("more"))
# async def searching(message: Message):
#     try:
#         links = ""
#         message_text = f'''Інші варіанти: '''
#
#         if len(list_car) <= 10:
#             for i in list_car:
#                 links += i.link + '\n' + '\n'
#             message_text += message_text + '\n' + links + '''\n '''
#         else:
#             for i in range(0, 10):
#                 links += list_car[i].link + '\n' + '\n'
#             list_car = list_car[10:]
#             message_text += message_text + '\n' + links + '\n' + '''Щоб подивить більше: /more'''
#
#     except:
#         message_text = f'''
#         Щось пішло не так(((
#
#         Щоб почати щераз напишіть: /set
#
#         '''
#
#     await message.answer(
#         text=message_text,
#         reply_markup=ReplyKeyboardRemove(),
#         parse_mode="html"
#     )