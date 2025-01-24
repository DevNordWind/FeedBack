import enum


class TicketStatus(str, enum.Enum):
    PENDING = "PENDING"
    ANSWERED = "ANSWERED"
    REJECTED = "REJECTED"
    BANNED = "BANNED"

