from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Select
from aiogram_dialog.widgets.text import Format

from src.bot.states import ProfileState
from src.bot.widgets import GetText
from .getter import profile_getter, ch_lg_getter
from .callable import on_ch_lg


profile = Window(
    GetText(
        'profile'
    ),

    SwitchTo(
        text=GetText('profile.ch-lg-btn'),
        state=ProfileState.ch_lg,
        id='ch_lg'
    ),


    getter=profile_getter,
    state=ProfileState.profile
)

ch_lg_window = Window(
    GetText('ch-lg'),

    Select(
        Format('{item[0]}'),
        id='lang_select_items',
        on_click=on_ch_lg,
        item_id_getter=lambda x: x[1],
        items='btns'
    ),

    SwitchTo(
        GetText(
            'back-btn'
        ),
        id='back_btn',
        state=ProfileState.profile
    ),

    getter=ch_lg_getter,
    state=ProfileState.ch_lg
)
