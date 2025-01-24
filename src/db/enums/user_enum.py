import enum


class Role(str, enum.Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    USER = "USER"


class LangCode(str, enum.Enum):
    RU = "RU"
    EN = "EN"
