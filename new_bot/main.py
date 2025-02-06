import asyncio
from aiogram import Bot, Dispatcher
from app.hendlers import router
# import logging



bot = Bot('8146626914:AAGPSN69kFklc95bNFqHtDmtllCiCnEKSfQ')
dp = Dispatcher()

async def main():
    # logging.basicConfig(level=logging.INFO)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')