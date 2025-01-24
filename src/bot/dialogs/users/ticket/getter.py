from aiogram_dialog import DialogManager

from src.bot.injections import inject_getter


@inject_getter
async def create_ticket_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return dialog_manager.dialog_data
