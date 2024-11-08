from site_parse import scrapy_parse_car
from car_obj import car_obj
import aiogram
import asyncio
from aiogram import Bot, Dispatcher
from handlers import questions





async def main():
    bot = Bot(token="")
    dp = Dispatcher()

    dp.include_router(questions.router)

    # And the run events dispatching
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

