from aiogram_dialog import Dialog

from .window import ticket_window, ticket_browsing, answer, answer_approve, ban, ban_approve, select_time, deny, \
    deny_approve

ticket_panel_dialog = Dialog(
    ticket_window,
    ticket_browsing,
    answer,
    answer_approve,
    ban,
    ban_approve,
    select_time,
    deny,
    deny_approve
)
