import json
import os
from typing import AsyncIterable

from adaptix import Retort
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.enums import ParseMode
from aiogram.types import TelegramObject
from dishka import Provider, Scope, provide, from_context
from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator, TranslatorRunner
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession

from src.bot.dispatcher import get_redis_storage, get_dispatcher
from src.configuration import conf
from src.db import Database, RedisUser


class AioProvider(Provider):
    telegram_object = from_context(
        provides=TelegramObject,
        scope=Scope.REQUEST,
    )

    event_context = from_context(
        provides=EventContext,
        scope=Scope.REQUEST
    )

    @provide(scope=Scope.APP)
    async def get_bot(self) -> Bot:
        return Bot(token=conf.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    @provide(scope=Scope.APP)
    async def get_dp(self, redis: Redis, translator: TranslatorHub) -> Dispatcher:
        return get_dispatcher(storage=get_redis_storage(redis=redis), translator=translator)


class DatabaseProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncEngine:
        return create_async_engine(url=conf.db.build_connection_str(), echo=conf.log.is_debug(), pool_pre_ping=True)

    @provide
    async def get_db(self, engine: AsyncEngine) -> AsyncIterable[Database]:
        async with AsyncSession(bind=engine) as session:
            yield Database(session=session)


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis(self) -> Redis:
        return Redis(
            db=conf.redis.db,
            host=conf.redis.host,
            password=conf.redis.passwd,
            username=conf.redis.username,
            port=conf.redis.port,
            decode_responses=True
        )

    @provide(scope=Scope.REQUEST)
    async def get_redis_user(self, redis: Redis, event_context: EventContext, retort: Retort) -> RedisUser:
        r_query = await redis.get(f'user:{event_context.user.id}')
        if not r_query:
            return None
        return retort.load(json.loads(r_query), RedisUser)


def get_ftl_files(locale: str) -> list:
    ftl_files = []
    path = f'./src/texts/{locale}/'
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.ftl'):
                ftl_files.append(os.path.join(root, file))
    return ftl_files


class TranslatorProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_translator_hub(self) -> TranslatorHub:
        return TranslatorHub(

            root_locale='ru',
            locales_map={
                "ru": ("ru",),
                "en": ("en", "ru"),
            },
            translators=
            [
                FluentTranslator(
                    locale='ru',
                    translator=FluentBundle.from_files(
                        "ru-RU",
                        filenames=get_ftl_files(locale='ru')),

                ),
                FluentTranslator(
                    locale='en',
                    translator=FluentBundle.from_files(
                        "en-US",
                        filenames=get_ftl_files(locale='en')),

                ),
            ]
        )

    @provide(scope=Scope.REQUEST)
    async def get_translator_runner(self, t_hub: TranslatorHub, event_context: EventContext, redis_user: RedisUser) -> TranslatorRunner:
        return t_hub.get_translator_by_locale(
            locale=redis_user.lang_code.value.lower() if redis_user and redis_user.lang_code else event_context.user.language_code
        )


class AdaptixProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_retort(self) -> Retort:
        return Retort()
