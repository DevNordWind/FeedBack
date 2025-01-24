import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import CONTAINER_NAME
from fluentogram import TranslatorRunner
from redis.asyncio import Redis

from src.bot.dialogs.root import start_external_place
from src.db import RedisUser


async def on_exception(event: ErrorEvent, **data):
    logging.error("Error: %s", event.exception)
    bot: Bot = data['bot']
    event_context: EventContext = data['event_context']
    dialog_manger: DialogManager = data['dialog_manager']
    with suppress(Exception):
        await dialog_manger.done()

    translator: TranslatorRunner = await data[CONTAINER_NAME].get(TranslatorRunner)
    redis_user: RedisUser = await data[CONTAINER_NAME].get(RedisUser)
    await bot.send_message(
        chat_id=event_context.user.id,
        text=translator.get('errors.unknown_error')
    )
    if event.update.message:
        return await start_external_place(
            event=event.update.message,
            translator=translator,
            redis_user=redis_user
        )
    if event.update.callback_query:
        return await start_external_place(
            event=event.update.callback_query.message,
            translator=translator,
            redis_user=redis_user
        )