from aiogram.filters import Filter
from aiogram.types import TelegramObject
from dishka import AsyncContainer

from src.db import RedisUser
from src.db.enums import Role


class IsAdminFilter(Filter):
    async def __call__(self, event: TelegramObject, dishka_container: AsyncContainer) -> bool:
        redis_user = await dishka_container.get(RedisUser)
        return Role.ADMINISTRATOR == redis_user.role
