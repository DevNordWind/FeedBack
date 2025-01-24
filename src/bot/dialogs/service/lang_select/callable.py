import json
from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from dishka import FromDishka
from fluentogram import TranslatorRunner, TranslatorHub
from redis.asyncio import Redis

from src.bot.dialogs.root import start_external_place
from src.bot.injections import inject_on_click
from src.bot.states import LangSelectState
from src.db import RedisUser, Database
from src.db.enums import LangCode
from src.db.models import User


async def start_lang_select(event: Message | CallbackQuery, dialog_manager: DialogManager):
    return await dialog_manager.start(
        state=LangSelectState.lang_select,
        mode=StartMode.RESET_STACK
    )


@inject_on_click
async def on_lang_select(
        event: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        item_id: str,
        db: FromDishka[Database],
        redis: FromDishka[Redis],
        translator_hub: FromDishka[TranslatorHub],
        redis_user: FromDishka[RedisUser],
        **kwargs
):
    lang_code = LangCode(item_id)

    await db.user.update(User.id == redis_user.id, {'lang_code': lang_code})
    redis_user.lang_code = lang_code

    await redis.set(f'user:{event.from_user.id}', value=json.dumps(redis_user.__dict__))
    await db.session.commit()

    await dialog_manager.done()
    await event.message.delete()

    return await start_external_place(
        event=event.message,
        translator=translator_hub.get_translator_by_locale(locale=lang_code.value.lower()),
        redis_user=redis_user
    )





