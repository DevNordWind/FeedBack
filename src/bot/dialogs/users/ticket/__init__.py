from aiogram_dialog import Dialog

from .window import create_ticket, ticket

from .callable import start_ticket

ticket_dialog = Dialog(
    create_ticket,
    ticket
)