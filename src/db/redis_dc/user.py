from dataclasses import dataclass
from typing import Optional

from src.db.enums import Role, LangCode


@dataclass
class RedisUser:
    id: int
    first_name: str
    role: Role
    last_name: Optional[str] = None
    username: Optional[str] = None
    lang_code: Optional[LangCode] = None
    is_banned: Optional[bool] = False
