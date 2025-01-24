from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from fluentogram import TranslatorRunner, TranslatorHub

from src.bot.injections import inject_on_click
from src.bot.states import TicketState
from src.bot.utls import admin_mailing
from src.db import Database, RedisUser
from src.db.models import Ticket


async def start_ticket(event: Message, dialog_manager: DialogManager):
    # await event.delete()
    return await dialog_manager.start(
        TicketState.ticket,
        # show_mode=ShowMode.DELETE_AND_SEND,
        mode=StartMode.RESET_STACK
    )


@inject_on_click
async def on_ticket(event: Message, widget: Any, dialog_manager: DialogManager, input_text: str, **kwargs):
    dialog_manager.dialog_data.update(
        {
            'question': input_text
        }
    )
    return await dialog_manager.switch_to(TicketState.create_ticket)


@inject_on_click
async def on_create_ticket_right(
        event: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        db: FromDishka[Database],
        redis_user: FromDishka[RedisUser],
        translator: FromDishka[TranslatorRunner],
        t_hub: FromDishka[TranslatorHub]
):
    bot, event_context = dialog_manager.middleware_data['bot'], dialog_manager.middleware_data['event_context']
    ticket: Ticket = await db.ticket.new(
        user_id_fk=redis_user.id,
        question=dialog_manager.dialog_data['question'],
    )
    await db.session.flush()

    await event.message.edit_text(
        translator.get('ticket.success-sent', ticket_id=ticket.id)
    )

    await admin_mailing(
        bot=bot,
        db=db,
        key='ticket.admin-msg',
        translator=t_hub,
        ticket_id=ticket.id,
        first_name=redis_user.first_name,
        user_id=str(event_context.user.id),
        created_at=ticket.created_at.strftime("%d.%m %H:%M"),
        question=ticket.question
    )

    await db.session.commit()

    await dialog_manager.done()
