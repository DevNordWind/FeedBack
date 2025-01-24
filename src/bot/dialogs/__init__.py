from .users import profile_dialog, start_profile, start_ticket, ticket_dialog
from .root import on_start
from .admins import ticket_panel_dialog, admin_root_dialog, admin_stat_dialog
from .service import on_ban, on_exception, lang_select_dialog

service_dialogs = (
    lang_select_dialog,
)

user_dialogs = (
    profile_dialog,
    ticket_dialog
)

admin_dialogs = (
    admin_root_dialog,
    ticket_panel_dialog,
    admin_stat_dialog
)