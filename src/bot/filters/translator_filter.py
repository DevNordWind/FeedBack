from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from dishka import AsyncContainer
from fluentogram import TranslatorRunner


class TranslatorFilter(BaseFilter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, event: TelegramObject, dishka_container: AsyncContainer, **data: Any) -> bool:
        t_runner = await dishka_container.get(TranslatorRunner)
        return t_runner.get(self.key) == event.text
