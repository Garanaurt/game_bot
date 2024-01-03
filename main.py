import asyncio
from aiogram import Bot, Dispatcher
from handlers.admin import hd_admin
from handlers.shop import shop


#Група на яку має бути підписаний користувач
MYGROUP = '@membertestchane'


#Токен для адмінки
TOKEN = '6275915048:AAFjJo5swSwJBTMdCpy1oHG-crySYilSd5M'


#Токен основного бота
SHOP_TOKEN = '5756085358:AAEboc6ZRK1pkgCnB1hDL_WTNlUqlTDWNg0'



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