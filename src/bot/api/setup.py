from aiogram import Router
from dishka import AsyncContainer
from dishka.integrations.aiogram import AutoInjectMiddleware

from src.bot.middlewares import ContainerMiddleware


def setup_dishka(
    container: AsyncContainer,
    router: Router,
    *,
    auto_inject: bool = False,
) -> None:
    middleware = ContainerMiddleware(container)
    auto_inject_middleware = AutoInjectMiddleware()

    for observer in router.observers.values():
        observer.outer_middleware(middleware)
        if auto_inject and observer.event_name != 'update':
            observer.middleware(auto_inject_middleware)