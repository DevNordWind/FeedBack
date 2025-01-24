import asyncio

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from dishka import make_async_container

from src.configuration import conf
from src.providers import AioProvider, DatabaseProvider, RedisProvider, TranslatorProvider, AdaptixProvider
from .api import setup_dishka


async def main():
    async_container = make_async_container(
        AioProvider(),
        DatabaseProvider(),
        RedisProvider(),
        TranslatorProvider(),
        AdaptixProvider()
    )
    dp, bot = await async_container.get(Dispatcher), await async_container.get(Bot)
    setup_dishka(async_container, dp)
    setup_dialogs(dp)
    conf.log.get_basic_logging()
    await dp.start_polling(
        bot
    )


if __name__ == "__main__":
    asyncio.run(main())
