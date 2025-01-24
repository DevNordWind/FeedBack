from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram_dialog.api.entities import EventContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from fluentogram import TranslatorRunner
from redis.asyncio import Redis

from src.db import RedisUser
from src.db.enums import Role


def start_keyboard(translator: TranslatorRunner, is_admin: bool) -> ReplyKeyboardMarkup:
    keyboards = [
        [
            KeyboardButton(
                text=translator.get('start.create-ticket-btn'),
            ),
            KeyboardButton(
                text=translator.get('start.profile-btn')
            )
        ],
    ]
    if is_admin:
        keyboards.append(
            [
                KeyboardButton(
                    text=translator.get('start.admin-btn')
                )
            ]
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboards, is_persistent=True, resize_keyboard=True
    )


@inject
async def on_start(
        event: Message,
        translator: FromDishka[TranslatorRunner],
        redis_user: FromDishka[RedisUser],
):
    return await event.answer(
        text=translator.get('start'),
        reply_markup=start_keyboard(
            translator,
            is_admin=Role.ADMINISTRATOR == redis_user.role
        )
    )


async def send_local_photo(event: Message, redis: Redis, role: Role, translator: TranslatorRunner) -> str:
    photo = FSInputFile(
        './src/images/start_photo.jpg'
    )
    sent_photo = await event.answer_photo(
        photo=photo,
        caption=translator.get('start'),
        reply_markup=start_keyboard(
            translator,
            is_admin=Role.ADMINISTRATOR == role
        )
    )
    return await redis.set(
        'start_photo', sent_photo.photo[0].file_id
    )


async def start_external_place(
        event: Message,
        translator: TranslatorRunner,
        redis_user: RedisUser
):
    return await event.answer(
        text=translator.get('start'),
        reply_markup=start_keyboard(
            translator,
            is_admin=Role.ADMINISTRATOR == redis_user.role
        )
    )