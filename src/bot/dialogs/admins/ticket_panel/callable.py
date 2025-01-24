import json
import traceback
from contextlib import suppress
from datetime import datetime, timedelta
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from dishka import FromDishka
from fluentogram import TranslatorRunner, TranslatorHub
from redis.asyncio import Redis

from src.bot.injections import inject_on_click
from src.bot.states import AdminStateTicket
from src.bot.utls import get_null_if_key_error
from src.db import Database, RedisUser
from src.db.enums import TicketStatus, ActionType
from src.db.models import User, Ticket


@inject_on_click
async def on_ticket(event: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str,
                    db: FromDishka[Database]):
    ticket_select = await db.ticket.get_by_where(Ticket.id == int(item_id))
    ticket_user = await db.user.get_by_where(User.id == int(ticket_select.user_id_fk))
    dialog_manager.dialog_data.update(
        {
            'ticket_id': ticket_select.id,
            'first_name': ticket_user.first_name,
            'user_id': str(ticket_user.user_id),
            'created_at': ticket_select.created_at.strftime("%H:%M %d.%m"),
            'question': ticket_select.question
        }
    )
    return await dialog_manager.switch_to(AdminStateTicket.browsing)


async def on_answer_approve(event: Message, widget: Any, dialog_manager: DialogManager, text_input: str):
    dialog_manager.dialog_data.update(
        {
            'answer': text_input
        }
    )
    return await dialog_manager.switch_to(AdminStateTicket.answer_approve)


@inject_on_click
async def on_answer(
        event: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        db: FromDishka[Database],
        t_hub: FromDishka[TranslatorHub],
        translator: FromDishka[TranslatorRunner],
        admin_user: FromDishka[RedisUser]
):
    bot = dialog_manager.middleware_data['bot']
    ticket = await db.ticket.get_by_where(Ticket.id == int(dialog_manager.dialog_data['ticket_id']))
    ticket_user = await db.user.get_by_where(User.id == Ticket.user_id_fk)
    ticket.status = TicketStatus.ANSWERED
    admin_action = await db.admin_action.new(
        ticket_id_fk=ticket.id,
        admin_id_fk=admin_user.id,
        action_type=ActionType.ANSWER,
        details=dialog_manager.dialog_data['answer']
    )

    with suppress(Exception):
        await bot.send_message(
            chat_id=ticket_user.user_id,
            text=t_hub.get_translator_by_locale(locale=ticket_user.lang_code.lower()).get('ticket-answer.notify-user',
                                                                                          ticket_id=ticket.id,
                                                                                          answer=admin_action.details)
        )
    await event.answer(translator.get('ticket-answer.notify-admin'), show_alert=True)
    await db.session.commit()
    await dialog_manager.switch_to(
        AdminStateTicket.admin_ticket
    )


async def on_deny(event: Message, widget: Any, dialog_manager: DialogManager, answer: str):
    dialog_manager.dialog_data.update(
        {
            'answer': answer
        }
    )
    await dialog_manager.switch_to(AdminStateTicket.deny_approve)


@inject_on_click
async def on_deny_approve(
        event: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        db: FromDishka[Database],
        translator: FromDishka[TranslatorRunner],
        t_hub: FromDishka[TranslatorHub]
):
    bot = dialog_manager.middleware_data['bot']
    ticket = await db.ticket.get_by_where(Ticket.id == int(dialog_manager.dialog_data['ticket_id']))
    admin_user = await db.user.get_by_where(User.user_id == event.from_user.id)
    ticket_user = await db.user.get_by_where(User.id == Ticket.user_id_fk)
    ticket.status = TicketStatus.REJECTED
    admin_action = await db.admin_action.new(
        ticket_id_fk=ticket.id,
        admin_id_fk=admin_user.id,
        action_type=ActionType.REJECT,
        details=dialog_manager.dialog_data['answer']
    )
    with suppress(Exception):
        await bot.send_message(
            chat_id=ticket_user.user_id,
            text=t_hub.get_translator_by_locale(locale=ticket_user.lang_code.lower()).get('ticket-deny.notify-user',
                                                                                          ticket_id=ticket.id,
                                                                                          answer=admin_action.details)
        )
    await event.answer(text=translator.get('ticket-deny.notify-admin'), show_alert=True)
    await db.session.commit()
    await dialog_manager.switch_to(
        AdminStateTicket.admin_ticket
    )


@inject_on_click
async def on_ban_reason(event: Message, widget: Any, dialog_manager: DialogManager, message_input: str):
    dialog_manager.dialog_data.update(
        {
            'reason': message_input
        }
    )

    return await dialog_manager.switch_to(AdminStateTicket.ban_approve)


async def on_time_select(event: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update({
        'time_unit': item_id
    }
    )

    return await dialog_manager.switch_to(AdminStateTicket.select_time)


async def on_time_input(event: CallbackQuery, widget: Any, dialog_manager: DialogManager, input: str):
    keys = ['days', 'hours', 'minutes']

    dialog_manager.dialog_data.update(
        {
            dialog_manager.dialog_data['time_unit']: input,
        }
    )
    until_date = datetime.now() + timedelta(**generate_time_dict(data=dialog_manager.dialog_data, keys=keys))
    dialog_manager.dialog_data.update(
        {
            'date_until': until_date.strftime("%d.%m.%Y %H:%M")
        }
    )
    return await dialog_manager.switch_to(
        AdminStateTicket.ban_approve
    )


def generate_time_dict(data: dict, keys: list[str]) -> dict:
    to_return = {}
    for key in keys:
        to_return.update(
            {
                key: get_null_if_key_error(data, key)
            }
        )
    return to_return


@inject_on_click
async def on_ban_send(
        event: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        db: FromDishka[Database],
        translator: FromDishka[TranslatorRunner],
        redis: FromDishka[Redis],
        t_hub: FromDishka[TranslatorHub],
):
    bot = dialog_manager.middleware_data['bot']
    ticket = await db.ticket.get_by_where(Ticket.id == int(dialog_manager.dialog_data['ticket_id']))
    admin_user = await db.user.get_by_where(User.user_id == event.from_user.id)
    ticket_user = await db.user.get_by_where(User.id == Ticket.user_id_fk)
    ticket_user.is_banned = True
    ticket.status = TicketStatus.BANNED
    admin_action = await db.admin_action.new(
        ticket_id_fk=ticket.id,
        admin_id_fk=admin_user.id,
        action_type=ActionType.BAN,
    )
    await db.session.flush()
    ban = await db.ban.new(
        user_id_fk=ticket.user_id_fk,
        ticket_id=ticket.id,
        admin_action_id=admin_action.id,
        reason=dialog_manager.dialog_data['reason'],
        until=datetime.strptime(dialog_manager.dialog_data['date_until'], "%d.%m.%Y %H:%M")
    )
    await bot.send_message(
        chat_id=ticket_user.user_id,
        text=t_hub.get_translator_by_locale(locale=ticket_user.lang_code.lower()).get('ticket-ban.notify-user',
                                                                                      ticket_id=ticket.id,
                                                                                      reason=ban.reason,
                                                                                      date_until=
                                                                                      dialog_manager.dialog_data[
                                                                                          'date_until'])
    )
    await redis.set(f'user:{ticket_user.user_id}', value=json.dumps(ticket_user.as_cache_dict()))
    await event.answer(text=translator.get('ticket-ban.notify-admin'), show_alert=True)
    await db.session.commit()
    dialog_manager.dialog_data.clear()
    await dialog_manager.switch_to(
        AdminStateTicket.admin_ticket
    )
