from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..models import Ban


class BanRepo(Repository[Ban]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=Ban, session=session)

    async def new(
            self,
            user_id_fk: int,
            ticket_id: int,
            admin_action_id: int,
            reason: str,
            until: datetime
    ) -> Ban:
        return await self.session.merge(
            Ban(
                user_id_fk=user_id_fk,
                ticket_id=ticket_id,
                admin_action_id=admin_action_id,
                reason=reason,
                until=until
            )
        )

    async def get_last_by_where(self, whereclause) -> Ban | None:
        stmt = select(Ban).where(whereclause).order_by(desc(Ban.id))
        return await self.session.scalar(stmt)
