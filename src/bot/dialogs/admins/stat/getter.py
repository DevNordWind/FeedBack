from aiogram_dialog import DialogManager
from dishka import FromDishka

from src.bot.injections import inject_getter
from src.db import Database
from src.db.enums import TicketStatus
from src.db.models import Ticket


@inject_getter
async def stat_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs) -> dict:
    user_amount = await db.user.count_all()
    ticket_amount = await db.ticket.count()
    ticket_pending_amount = await db.ticket.count(whereclause=Ticket.status == TicketStatus.PENDING)

    return {
        'users_amount': str(user_amount),
        'ticket_amount': str(ticket_amount),
        'ticket_pending_amount': str(ticket_pending_amount)
    }
