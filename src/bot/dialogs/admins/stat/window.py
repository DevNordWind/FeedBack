from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel

from src.bot.states import AdminStateStat
from src.bot.widgets import GetText
from .getter import stat_getter

admin_stat_window = Window(
    GetText(
        'admin-stat'
    ),

    Cancel(
        GetText(
            'back-btn'
        )
    ),

    getter=stat_getter,
    state=AdminStateStat.stat
)
