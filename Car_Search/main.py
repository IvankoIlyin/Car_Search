from site_parse import scrapy_parse_car
from car_obj import car_obj
import aiogram
import asyncio
from aiogram import Bot, Dispatcher
from handlers import questions


# car_char=car_obj.Car_Characteristics()
# car_char.add_attr("Тип палива","Бензин")
# car_char.add_attr("Коробка","Механіка")
# car_char.add_attr("Тип кузова","Хетчбек")
# car_char.add_attr("Тип кузова","Седан")
# car_char.add_attr("Тип кузова","Кросовер")
# car_char.add_attr("Привід","Передній")
# car_char.add_attr("Колір","Чорний")
# car_char.add_attr("Пробіг","300")
# car_char.add_attr("Двигун","2")
# car=car_obj.Car("skoda","octavia",["3000","10000"],["2000","2015"],car_char,"Продам авто Skoda Oktavia a 5 машина в хорошому стані мотор працює добре коробка передач супер масла фільтра замінені")
#
# # Color: Red,Black
# list = scrapy_parse_car.start_parse_car_site(car)
#
# for i in list:
#     print(i.link)


async def main():
    bot = Bot(token="6522837095:AAGpGmy2TBwrXadFC-lApyqFkgUcS3SFOV0")
    dp = Dispatcher()

    dp.include_router(questions.router)

    # And the run events dispatching
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

