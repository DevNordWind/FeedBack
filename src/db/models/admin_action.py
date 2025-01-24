import datetime

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..enums import ActionType


class AdminAction(Base):
    ticket_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('ticket.id')
    )
    admin_id: Mapped[int] = mapped_column(
        sa.ForeignKey('user.id')
    )

    action_type: Mapped[ActionType] = mapped_column(
        sa.String(length=32), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=func.now()
    )
    details: Mapped[str] = mapped_column(
        sa.String, nullable=True
    )

    ticket: Mapped["Ticket"] = relationship(
        back_populates="admin_action",
        uselist=False
    )

    ban: Mapped["Ban"] = relationship(
        back_populates='admin_action',
        uselist=False
    )
