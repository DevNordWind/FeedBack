from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Start

from src.bot.states import AdminState, AdminStateTicket, AdminStateStat
from src.bot.widgets import GetText

admin_root = Window(
    GetText(
        'admin-root'
    ),

    Start(
        GetText(
            'admin-root.tickets-btn',
        ),
        state=AdminStateTicket.admin_ticket,
        id='to_ticket'
    ),

    Start(
        GetText(
            'admin-root.stat-btn'
        ),
        state=AdminStateStat.stat,
        id='to_stat'
    ),

    state=AdminState.admin
)
