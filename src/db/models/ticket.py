import datetime

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..enums import TicketStatus


class Ticket(Base):
    user_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('user.id'),
    )

    question: Mapped[str] = mapped_column(
        sa.String, nullable=False
    )

    status: Mapped[TicketStatus] = mapped_column(
        sa.String(length=32), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=func.now()
    )

    user: Mapped["User"] = relationship(
        back_populates='ticket',
        uselist=False
    )

    admin_action: Mapped["AdminAction"] = relationship(
        back_populates='ticket',
        uselist=False
    )

    ban: Mapped["Ban"] = relationship(
        back_populates='ticket',
        uselist=False
    )
