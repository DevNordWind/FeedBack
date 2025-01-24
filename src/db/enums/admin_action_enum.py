import enum


class ActionType(str, enum.Enum):
    ANSWER = "ANSWER"
    REJECT = "REJECT"
    BAN = "BAN"
