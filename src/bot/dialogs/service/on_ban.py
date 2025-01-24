import json
from datetime import datetime

import redis.commands.core
from aiogram import Bot
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from fluentogram import TranslatorRunner
from redis.asyncio import Redis

from src.db import Database, RedisUser
from src.db.models import Ban, User


@inject
async def on_ban(event: CallbackQuery | Message, bot: Bot,
                 event_context: EventContext,
                 db: FromDishka[Database],
                 translator: FromDishka[TranslatorRunner],
                 redis: FromDishka[Redis],
                 redis_user: FromDishka[RedisUser]
                 ):
    ban = await db.ban.get_last_by_where(
        Ban.user_id_fk == redis_user.id
    )
    if datetime.now() >= ban.until:
        redis_user.is_banned = False
        await redis.set(f'user:{event_context.user.id}', value=json.dumps(redis_user.__dict__))
        await db.user.update(User.id == redis_user.id, values={'is_banned': False})
        return await bot.send_message(
            chat_id=event.from_user.id,
            text=translator.get(
                'on-ban-expired'
            )
        )

    return await bot.send_message(
        chat_id=event_context.user.id,
        text=translator.get(
            'on-ban',
            ticket_id=ban.ticket_id,
            reason=ban.reason,
            date_until=ban.until.strftime("%H:%M %d.%m")
        ),
        reply_markup=ReplyKeyboardRemove()
    )
