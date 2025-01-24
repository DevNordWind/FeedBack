from aiogram_dialog import Dialog

from .ticket_panel import ticket_panel_dialog
from .window import admin_root
from .callable import start_admin
from .stat import admin_stat_dialog
admin_root_dialog = Dialog(admin_root)


