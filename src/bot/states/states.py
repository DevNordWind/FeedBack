from aiogram.fsm.state import StatesGroup, State


class StartState(StatesGroup):
    start = State()


class TicketState(StatesGroup):
    ticket = State()
    create_ticket = State()


class ProfileState(StatesGroup):
    profile = State()
    ch_lg = State()


class AdminState(StatesGroup):
    admin = State()


class AdminStateTicket(StatesGroup):
    admin_ticket = State()
    browsing = State()
    answer = State()
    answer_approve = State()
    deny = State()
    deny_approve = State()
    ban = State()
    ban_approve = State()
    select_time = State()


class AdminStateStat(StatesGroup):
    stat = State()


class LangSelectState(StatesGroup):
    lang_select = State()
