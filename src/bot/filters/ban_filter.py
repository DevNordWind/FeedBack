from aiogram.filters import Filter
from aiogram.types import TelegramObject
from dishka import AsyncContainer

from src.db import RedisUser


class BanFilter(Filter):
    async def __call__(self, event: TelegramObject, dishka_container: AsyncContainer) -> bool:
        redis_user = await dishka_container.get(RedisUser)
        if redis_user and redis_user.is_banned:
            return True
        return False
