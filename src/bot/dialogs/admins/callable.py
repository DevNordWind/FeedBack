from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.bot.states import AdminState


async def start_admin(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        AdminState.admin,
        mode=StartMode.RESET_STACK
    )
