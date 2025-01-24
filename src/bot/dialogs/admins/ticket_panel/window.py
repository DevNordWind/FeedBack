from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Column, Select, ScrollingGroup, Group, Button, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Format

from src.bot.states import AdminStateTicket
from src.bot.widgets import GetText
from .getter import browsing_getter, answer_approve_getter, admin_ticket_getter, ban_approve_getter, select_time_getter

SCROLL_ID = 'TICKET_ADMIN_SCROLL'

from .callable import on_ticket, on_answer_approve, on_answer, on_deny, on_deny_approve, on_ban_reason, on_time_select, \
    on_time_input, on_ban_send

ticket_window = Window(
    GetText('admin-ticket'),

    ScrollingGroup(
        Column(
            Select(
                text=Format('🎫 Тикет #{item.id} | ⌛️ {item.created_at}'),
                item_id_getter=lambda ticket: ticket.id,
                on_click=on_ticket,
                items='tickets',
                id='ticket_select'
            ),
        ),
        width=1,
        height=8,
        id=SCROLL_ID
    ),

    Cancel(
        GetText('back-btn'),
    ),

    getter=admin_ticket_getter,
    state=AdminStateTicket.admin_ticket
)

ticket_browsing = Window(
    GetText(
        'ticket-browsing'
    ),
    Group(
        SwitchTo(
            GetText('ticket-browsing.process-btn'),
            id='process',
            state=AdminStateTicket.answer
        ),
        SwitchTo(
            GetText('ticket-browsing.deny-btn'),
            state=AdminStateTicket.deny,
            id='deny'
        ),
        width=2
    ),

    SwitchTo(
        GetText('ticket-browsing.ban-btn'),
        id='ban',
        state=AdminStateTicket.ban
    ),

    SwitchTo(
        GetText('back-btn'),
        id='back',
        state=AdminStateTicket.admin_ticket
    ),

    getter=browsing_getter,
    state=AdminStateTicket.browsing
)

answer = Window(
    GetText(
        'ticket-answer'
    ),
    TextInput(
        on_success=on_answer_approve,
        id='answer'
    ),

    SwitchTo(
        GetText('back-btn'),
        id='back',
        state=AdminStateTicket.browsing
    ),

    state=AdminStateTicket.answer
)

answer_approve = Window(
    GetText(
        'ticket-answer.approve'

    ),

    Button(
        GetText('right-btn'),
        id='success_approve',
        on_click=on_answer,
    ),

    SwitchTo(
        GetText('back-btn'),
        id='back',
        state=AdminStateTicket.answer
    ),
    getter=answer_approve_getter,
    state=AdminStateTicket.answer_approve
)

deny = Window(
    GetText(
        'ticket-deny'
    ),

    TextInput(
        id='deny',
        on_success=on_deny
    ),

    SwitchTo(
        GetText('back-btn'),
        id='back',
        state=AdminStateTicket.deny
    ),

    state=AdminStateTicket.deny
)

deny_approve = Window(
    GetText(
        'approve'
    ),

    Button(
        GetText('right-btn'),
        id='success_approve',
        on_click=on_deny_approve,
    ),

    SwitchTo(
        GetText(
            'back-btn'
        ),
        id='back',
        state=AdminStateTicket.deny
    ),
    getter=answer_approve_getter,
    state=AdminStateTicket.deny_approve
)

ban = Window(
    GetText(
        'ticket-ban'
    ),

    TextInput(
        id='ban_answer',
        on_success=on_ban_reason
    ),

    SwitchTo(
        GetText(
            'back-btn'
        ),
        id='back',
        state=AdminStateTicket.browsing
    ),

    state=AdminStateTicket.ban
)

ban_approve = Window(
    GetText(
        'ticket-ban.select-time'
    ),
    Select(
        text=Format('{item.name}'),
        items='btns',
        item_id_getter=lambda x: x.id,
        on_click=on_time_select,
        id='time'
    ),

    Button(
        GetText(
            'ticket-ban.ban-btn',
        ),
        on_click=on_ban_send,
        id='send_ban'
    ),

    SwitchTo(
        GetText(
            'back-btn'
        ),
        id='back',
        state=AdminStateTicket.ban
    ),

    getter=ban_approve_getter,
    state=AdminStateTicket.ban_approve
)

select_time = Window(
    GetText(
        'ticket-ban.input-time'
    ),

    TextInput(
        id='time_input',
        on_success=on_time_input,
    ),

    SwitchTo(
        GetText(
            'back-btn'
        ),
        id='back',
        state=AdminStateTicket.ban_approve
    ),

    getter=select_time_getter,
    state=AdminStateTicket.select_time
)
