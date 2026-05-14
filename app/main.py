import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from aiohttp_socks import ProxyConnector

from app.config import BOT_TOKEN, PROXY_URL
from app.handlers.status import router


async def main():

    if PROXY_URL:
        connector = ProxyConnector.from_url(PROXY_URL)
        session = AiohttpSession(connector=connector)
    else:
        session = AiohttpSession()

    bot = Bot(
        token=BOT_TOKEN,
        session=session
    )

    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())