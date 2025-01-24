from dataclasses import dataclass

from aiogram_dialog import DialogManager
from dishka import FromDishka
from fluentogram import TranslatorRunner

from src.bot.injections import inject_getter
from src.db import Database
from src.db.enums import TicketStatus
from src.db.models import Ticket


@dataclass
class TicketSelect:
    id: str
    user_id_fk: str
    question: str
    status: TicketStatus
    created_at: str


@dataclass
class TimeSelect:
    id: str
    name: str


@inject_getter
async def admin_ticket_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    tickets = await db.ticket.get_many(
        whereclause=Ticket.status == TicketStatus.PENDING,
        order_by=Ticket.id
    )
    tickets = [TicketSelect(id=str(ticket.id), user_id_fk=str(ticket.user_id_fk), question=ticket.question,
                            status=ticket.status,
                            created_at=ticket.created_at.strftime("%H:%M %d.%m")) for ticket in
               tickets] if tickets else []

    return {
        'tickets': tickets,
        'is_tickets_exists': str(True) if tickets != [] else False
    }


async def browsing_getter(dialog_manager: DialogManager, **kwargs):
    return dialog_manager.dialog_data


async def answer_approve_getter(dialog_manager: DialogManager, **kwargs):
    return dialog_manager.dialog_data


@inject_getter
async def ban_approve_getter(dialog_manager: DialogManager, translator: FromDishka[TranslatorRunner], **kwargs):
    keys = ['days', 'hours', 'minutes']
    return {
        'btns': [TimeSelect(id=key, name=translator.get(f'ticket-ban.{key}-btn')) for key in keys],
        'is_time_selected': str(any(key in dialog_manager.dialog_data for key in keys)),
        **dialog_manager.dialog_data
    }


async def select_time_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return dialog_manager.dialog_data
