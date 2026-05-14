import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from app.config import BOT_TOKEN, PROXY_URL
from app.db.database import init_db
from app.handlers.status import router as status_router
from app.handlers.maintenance import router as maintenance_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


async def main():
    logger.info("Initializing database...")
    await init_db()

    logger.info("Starting bot...")

    if PROXY_URL:
        logger.info("Proxy enabled")
        session = AiohttpSession(proxy=PROXY_URL)
    else:
        logger.info("Proxy disabled")
        session = AiohttpSession()

    bot = Bot(token=BOT_TOKEN, session=session)

    me = await bot.get_me()
    logger.info(f"Bot authorized: @{me.username} ({me.id})")

    dp = Dispatcher()

    dp.include_router(status_router)
    dp.include_router(maintenance_router)

    logger.info("Starting polling...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())