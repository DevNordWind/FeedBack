from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button

from src.bot.states import TicketState
from src.bot.widgets import GetText
from .callable import on_ticket, on_create_ticket_right
from .getter import create_ticket_getter

ticket = Window(
    GetText(
        'ticket'
    ),

    TextInput(
        id='text_input',
        on_success=on_ticket
    ),

    state=TicketState.ticket
)

create_ticket = Window(
    GetText(
        'ticket.create-ticket'
    ),

    Button(
        GetText(
            'right-btn'
        ),
        on_click=on_create_ticket_right,
        id='right'
    ),

    SwitchTo(
        GetText('back-btn'),
        state=TicketState.ticket,
        id='back'
    ),
    state=TicketState.create_ticket,
    getter=create_ticket_getter
)
