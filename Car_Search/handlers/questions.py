from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from car_obj import car_obj
from keyboards.simple_row import make_row_keyboard
from site_parse import scrapy_parse_car

car=car_obj.Car()


router = Router()  # [1]

other = "Інше"

available_salesmans = ["Компанія", "Автодилер","Власник", other]
available_transmissions = ["Автомат", "Механіка","Типтронік","Варіатор","Робот", other]
available_fuel_types = ["Дизель", "Бензин", "Газ","Електро","Водень","Гібрид", other]
available_drive_types = ["Передній", "Задній","Повний","Ланцюг","Кардан", other]
available_body_types = ["Купе", "Універсал","Седан","Позашляховик / Кросовер","Хетчбек", other]
available_colors = ["Чорний", "Синій", "Білий","Коричневий","Зелений ","Сірий","Помаранчевий","Фіолетовий","Червоний","Жовтий", other]


class UserState(StatesGroup):
    choosing_salesman = State()
    choosing_transmission = State()
    choosing_fuel_type = State()
    input_engine_capacity = State()
    choosing_drive_type = State()
    choosing_body_type = State()
    choosing_color = State()
    input_mileage = State()
    input_fuel_costs = State()
    input_location = State()
    input_title = State()
    input_years=State()
    input_price=State()
    input_description=State()

@router.message(Command("start"))
async def hello(message: Message):
    await message.answer(
        text="Привіт, я бот, що допоможе тобі знайти оптимальну пропозицію авто. Пиши дані коректно щоб отримати задовільну відповідь, Для початку напиши /set",
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
    # Встановлюємо користувачу стан "вибирає продавця"
    await state.set_state(UserState.choosing_salesman)


@router.message(UserState.choosing_salesman)
async def salesman_choosed(message: Message, state: FSMContext):
    await state.update_data(salesman=message.text.lower())
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
async def mileage_choosed(message: Message, state: FSMContext):
    await state.update_data(mileage=message.text)
    await message.answer(
        text="Витрати пального (л/100 км):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.input_fuel_costs)


@router.message(UserState.input_fuel_costs)
async def fuel_costs_choosed(message: Message, state: FSMContext):
    await state.update_data(fuel_costs=message.text)
    await message.answer(
        text="Місто:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.input_location)


@router.message(UserState.input_location)
async def location_choosed(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer(
        text="Опис:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(UserState.input_description)

@router.message(UserState.input_description)
async def description_choosed(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    data = await state.get_data()

    car_char = car_obj.Car_Characteristics()
    car_char.add_attr('Продавець', data["salesman"])
    car_char.add_attr('Коробка', data["transmission"])
    car_char.add_attr('Паливо', data["fuel_type"])
    car_char.add_attr('Двигун', data["engine_capacity"])
    car_char.add_attr('Привід', data["drive_type"])
    car_char.add_attr('Кузов', data["body_type"])
    car_char.add_attr('Колір', data["color"])
    car_char.add_attr('Пробіг', data["mileage"])
    car_char.add_attr('Витрати пального', data["fuel_costs"])
    car_char.add_attr('Місто', data["location"])

    title = data["title"].split(' ')
    mark, model = title[0], title[1]
    years = data["years"].split('-')
    price = data["price"].split('-')

    car.mark=mark
    car.model=model
    car.price=price
    car.year=years
    car.characteristics=car_char
    car.dedescription=data["description"]

    #car = Car(mark, model, price, years, car_char, data["description"])

    message_text = f'''
    
    Назва: <b>{data["title"]}</b>
    Ціна: <b>{data["price"]}</b>
    Роки: <b>{data["years"]}</b>
    
    Оголошення від: <b>{data["salesman"]}</b>
    Коробка передач: <b>{data["transmission"]}</b>
    Тип палива: <b>{data["fuel_type"]}</b>
    Двигун: <b>{data["engine_capacity"]}</b>
    Тип кузова: <b>{data["body_type"]}</b>
    Колір: <b>{data["color"]}</b>
    Пробіг: <b>{data["mileage"]}</b>
    Витрати пального: <b>{data["fuel_costs"]}</b>
    Місто: <b>{data["location"]}</b>
    Опис: <b>{data["description"]}</b>
    
    Якщо інформація НЕ ВІРНА почніть спочатку: /set
    
    Якщо інформація ВІРНА почніть спочатку: /search
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


    list = scrapy_parse_car.start_parse_car_site(car)
    links=""
    for i in list:
        links+=i.link+'\n'
    message_text = f'''ЗНАЙШЛИ!!! ''' + links + ''' Всіх благ братік'''

    await message.answer(
        text=message_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="html"
    )
