from aiogram_dialog import Dialog

from .window import profile, ch_lg_window

from .callable import start_profile

profile_dialog = Dialog(
    profile,
    ch_lg_window
)