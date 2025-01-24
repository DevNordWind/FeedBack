"""User model file."""
import datetime

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..enums import Role, LangCode


class User(Base):
    """User model."""

    """ Telegram user id """

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, nullable=False, unique=True
    )

    """ Telegram user_name (Optional) """
    username: Mapped[str] = mapped_column(
        sa.String(length=32), unique=True, nullable=True
    )

    """ Telegram first_name"""

    first_name: Mapped[str] = mapped_column(
        sa.String(length=64), nullable=False
    )

    """ Telegram last_name (Optional)"""

    last_name: Mapped[str] = mapped_column(
        sa.String(length=64), nullable=True
    )

    """ User role """

    role: Mapped[Role] = mapped_column(
        sa.String(length=32), nullable=False
    )

    """ User status """
    is_banned: Mapped[bool] = mapped_column(
        sa.Boolean, default=False, nullable=False
    )

    lang_code: Mapped[LangCode] = mapped_column(
        sa.String(length=6), nullable=True
    )

    """ Registration time """

    reg_time: Mapped[datetime] = mapped_column(
        sa.DateTime, default=func.now(), nullable=False
    )

    """ Relationships """

    ticket: Mapped[list["Ticket"]] = relationship(
        back_populates='user',
        uselist=True,
    )

    ban: Mapped["Ban"] = relationship(
        back_populates='user',
        uselist=False
    )

    def as_cache_dict(self) -> dict:
        data = self.__dict__
        data.pop('_sa_instance_state')
        data.pop('user_id')
        data.pop('reg_time')
        return data
