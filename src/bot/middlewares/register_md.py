"""Database middleware is a common way to inject database dependency in api_handler."""
import json
from collections.abc import Awaitable, Callable
from typing import Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, ErrorEvent
from aiogram.types import User as AioUser
from dishka import AsyncContainer
from dishka.integrations.aiogram import CONTAINER_NAME
from redis.asyncio import Redis

from src.configuration import conf
from src.db import Database, RedisUser
from src.db.models import User


class RegisterMD(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery | ErrorEvent,
            data: Dict
    ) -> Any:
        """This method calls every update."""
        aiogram_user: AioUser = data['event_context'].user
        async_container: AsyncContainer = data[CONTAINER_NAME]
        redis_user: RedisUser = await async_container.get(RedisUser)
        redis: Redis = await async_container.get(Redis)
        db: Database = await async_container.get(Database)
        if not redis_user:
            await self.register(aiogram_user, db, redis)
        else:
            await self.handle_user_data(aiogram_user, db, redis, redis_user)
        return await handler(event, data)

    async def register(self, aio_user: AioUser, db: Database, redis: Redis) -> RedisUser:
        role = conf.admins.get_role(aio_user.id)
        db_user = await db.user.get_by_where(User.user_id == aio_user.id)
        if not db_user:
            user = await db.user.new(
                user_id=aio_user.id,
                username=aio_user.username,
                first_name=aio_user.first_name,
                last_name=aio_user.last_name,
                role=role
            )
            await db.session.flush()
            await redis.set(
                f'user:{aio_user.id}', value=json.dumps(user.as_cache_dict())
            )
            await db.session.commit()
        else:
            await redis.set(
                f'user:{aio_user.id}', value=json.dumps(db_user.as_cache_dict())
            )

    async def handle_user_data(self,
                               aio_user: AioUser,
                               db: Database,
                               redis: Redis,
                               redis_user: RedisUser
                               ):
        keys = ['last_name', 'username']
        need_commit = False
        for key in keys:
            redis_atr = getattr(redis_user, key)
            aio_atr = getattr(aio_user, key)
            if redis_atr != aio_atr:
                need_commit = True
                data = {key: aio_atr}
                await db.user.update(User.id == redis_user.id, values=data)
                redis_user.__dict__.update(data)
                await redis.set(f'user:{aio_user.id}', value=json.dumps(redis_user.__dict__))
        if need_commit:
            await db.session.commit()
