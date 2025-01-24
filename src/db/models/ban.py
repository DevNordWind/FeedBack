from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Ban(Base):
    user_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('user.id')
    )
    ticket_id: Mapped[int] = mapped_column(
        sa.ForeignKey('ticket.id')
    )

    admin_action_id: Mapped[int] = mapped_column(
        sa.ForeignKey('adminaction.id')
    )

    reason: Mapped[str] = mapped_column(
        sa.String, nullable=False
    )

    until: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates='ban',
        uselist=False,
    )

    ticket: Mapped['Ticket'] = relationship(
        back_populates='ban',
        uselist=False
    )

    admin_action: Mapped['AdminAction'] = relationship(
        back_populates='ban',
        uselist=False
    )
