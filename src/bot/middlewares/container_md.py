from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.types import TelegramObject

from dishka import AsyncContainer
from dishka.integrations.aiogram import CONTAINER_NAME


class ContainerMiddleware(BaseMiddleware):
    def __init__(self, container: AsyncContainer) -> None:
        self.container = container

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        async with self.container({TelegramObject: event, EventContext: data['event_context']}) as sub_container:
            data[CONTAINER_NAME] = sub_container
            return await handler(event, data)
