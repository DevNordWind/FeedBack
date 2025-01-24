from aiogram.filters import Filter
from aiogram.types import TelegramObject, CallbackQuery
from aiogram_dialog.api.entities import Context
from dishka import AsyncContainer

from src.bot.states import LangSelectState
from src.db import RedisUser


class IsSelectLangFilter(Filter):
    async def __call__(self, event: TelegramObject, dishka_container: AsyncContainer, aiogd_context: Context, **data) -> bool:
        redis_user = await dishka_container.get(RedisUser)
        if redis_user and redis_user.lang_code is None:
            if isinstance(event, CallbackQuery):
                if aiogd_context.state == LangSelectState.lang_select:
                    return False
            return True
        return False
