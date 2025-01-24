from aiogram import Dispatcher, Bot, F
from aiogram.filters import CommandStart, ExceptionTypeFilter
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage, DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from .dialogs import user_dialogs, on_start, start_profile, start_ticket, admin_dialogs, service_dialogs, on_ban, \
    on_exception
from .dialogs.admins import start_admin
from .dialogs.service.lang_select.callable import start_lang_select
from .filters import TranslatorFilter, IsAdminFilter, IsSelectLangFilter, BanFilter
from .middlewares import *
from ..configuration import conf


def get_texts_by_key(translator: TranslatorHub, key: str) -> set[str]:
    texts_list = set()
    for locale in translator.locales_map.keys():
        texts_list.add(translator.get_translator_by_locale(locale).get(key))
    return texts_list



def get_dispatcher(
        storage: BaseStorage,
        translator: TranslatorHub,
        fsm_strategy: FSMStrategy = FSMStrategy.CHAT,
        event_isolation: BaseEventIsolation = None,
) -> Dispatcher:
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=fsm_strategy,
        events_isolation=event_isolation,
    )
    dp.error.register(on_exception, ExceptionTypeFilter(Exception))

    dp.message.outer_middleware(RegisterMD())
    dp.callback_query.outer_middleware(RegisterMD())
    dp.errors.outer_middleware(RegisterMD())

    dp.message.register(on_ban, BanFilter())
    dp.callback_query.register(on_ban, BanFilter())

    dp.message.register(start_lang_select, IsSelectLangFilter())
    dp.callback_query.register(start_lang_select, IsSelectLangFilter())

    dp.message.register(on_start, CommandStart())

    profile_texts = get_texts_by_key(translator, 'start.profile-btn')
    create_texts = get_texts_by_key(translator, 'start.create-ticket-btn')
    dp.message.register(start_profile, F.text.in_(profile_texts))
    dp.message.register(start_ticket, F.text.in_(create_texts))

    for dialog in service_dialogs:
        dp.include_router(dialog)

    for dialog in user_dialogs:
        dp.include_router(dialog)
    admin_texts = get_texts_by_key(translator, 'start.admin-btn')
    dp.message.register(start_admin, F.text.in_(admin_texts), IsAdminFilter())

    for dialog in admin_dialogs:
        dialog.message.filter(IsAdminFilter())
        dialog.callback_query.filter(IsAdminFilter())
        dp.include_router(dialog)

    dp.startup.register(on_startup)

    return dp


def get_redis_storage(
        redis: Redis, state_ttl=conf.redis.state_ttl, data_ttl=conf.redis.data_ttl
):
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl,
                        key_builder=DefaultKeyBuilder(with_destiny=True))


async def on_startup(bot: Bot):
    await set_commands(bot)


async def set_commands(bot: Bot):

    await bot.set_my_commands(
        commands=[
            BotCommand(
                command='start', description='♻️ Перезапустить бота',
            ),
        ],
        language_code='ru'
    )

    await bot.set_my_commands(
        commands=[
            BotCommand(
                command='start', description='♻️ Restart bot',
            ),
        ],
        language_code='en'
    )
