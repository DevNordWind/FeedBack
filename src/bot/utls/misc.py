from contextlib import suppress

from aiogram import Bot
from dishka import FromDishka
from fluentogram import TranslatorHub

from src.db import Database
from src.db.enums import Role
from src.db.models import User


async def admin_mailing(
        bot: Bot,
        db: FromDishka[Database],
        translator: TranslatorHub,
        key: str,
        reply_markup=None,
        **kwargs
):
    admins = await db.user.get_many(User.role == Role.ADMINISTRATOR)
    with suppress(Exception):
        for admin in admins:
            translator = translator.get_translator_by_locale(locale=admin.lang_code.lower())
            await bot.send_message(
                chat_id=admin.user_id,
                text=translator.get(key, **kwargs),
                reply_markup=reply_markup
            )


def get_null_if_key_error(data: dict, key: str) -> int:
    try:
        return int(data[key])
    except KeyError:
        return 0
    except TypeError:
        return 0
