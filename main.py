import asyncio
from aiogram import Bot, Dispatcher
from handlers.admin import hd_admin
from handlers.shop import shop


#Група на яку має бути підписаний користувач
MYGROUP = '@dzigari'


#Токен для адмінки
TOKEN = '6856469545:AAFd5FOUHO81w8T-g93goFmuXkbMzkIxswM'


#Токен основного бота
SHOP_TOKEN = '6850590181:AAE90MAY3O_OJxGaj6fqT1czsBZUICYqtJM'



async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(hd_admin.router)
    await bot.delete_webhook(drop_pending_updates=True)

    bot_s = Bot(token=SHOP_TOKEN)
    dpt = Dispatcher()
    dpt.include_routers(shop.router)
    await bot_s.delete_webhook(drop_pending_updates=True)

    tasks = [
        asyncio.create_task(dp.start_polling(bot)),
        asyncio.create_task(dpt.start_polling(bot_s))
    ]

    await asyncio.gather(*tasks)



if __name__ == "__main__":
    asyncio.run(main())