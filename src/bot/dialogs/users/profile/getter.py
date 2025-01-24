from aiogram_dialog import DialogManager
from dishka import FromDishka
from fluentogram import TranslatorRunner

from src.bot.injections import inject_getter
from src.db import Database, RedisUser
from src.db.enums import LangCode


@inject_getter
async def profile_getter(dialog_manager: DialogManager, db: FromDishka[Database], redis_user: FromDishka[RedisUser], **kwargs):
    user_id: int = dialog_manager.event.from_user.id
    reg_time, ticket_amount = (await db.user.get_user_profile(id=redis_user.id))[0]
    return {
        'reg_time': reg_time,
        'ticket_amount': ticket_amount,
        'user_id': str(user_id)
    }

@inject_getter
async def ch_lg_getter(dialog_manager: DialogManager, translator: FromDishka[TranslatorRunner], **kwargs) -> dict:
    prefix = 'lang-select'
    btns = [
        (translator.get(f'{prefix}.{lang_code.lower()}'), lang_code) for lang_code in LangCode.__members__
    ]
    return {
        'btns': btns
    }