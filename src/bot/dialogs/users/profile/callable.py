import json
from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from dishka import FromDishka
from fluentogram import TranslatorRunner, TranslatorHub
from redis.asyncio import Redis

from src.bot.dialogs.root import start_keyboard
from src.bot.injections import inject_on_click
from src.bot.states import ProfileState
from src.db import Database, RedisUser
from src.db.enums import LangCode, Role
from src.db.models import User


async def start_profile(event: Message, dialog_manager: DialogManager):
    # await event.delete()
    return await dialog_manager.start(
        ProfileState.profile,
        # show_mode=ShowMode.DELETE_AND_SEND,
        mode=StartMode.RESET_STACK
    )


@inject_on_click
async def on_ch_lg(
        event: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        item_id: str,
        db: FromDishka[Database],
        redis_user: FromDishka[RedisUser],
        redis: FromDishka[Redis],
        t_hub: FromDishka[TranslatorHub]
):
    lang_code = LangCode(item_id)
    if lang_code == redis_user.lang_code:
        return
    await db.user.update(User.id == redis_user.id, {'lang_code': lang_code})
    redis_user.lang_code = lang_code
    await redis.set(f'user:{event.from_user.id}', value=json.dumps(redis_user.__dict__))
    await change_keyboard(event=event.message,
                          translator=t_hub.get_translator_by_locale(locale=lang_code.value.lower()),
                          is_admin=Role.ADMINISTRATOR == redis_user.role)
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await db.session.commit()


async def change_keyboard(event: Message, translator: TranslatorRunner, is_admin: bool) -> Message:
    kb = start_keyboard(
        translator=translator,
        is_admin=is_admin
    )
    return await event.reply(
        translator.get('lang-select.ch_kb'),
        reply_markup=kb
    )
