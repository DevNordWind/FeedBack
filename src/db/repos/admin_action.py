from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..enums import ActionType
from ..models import AdminAction


class AdminActionRepo(Repository[AdminAction]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=AdminAction, session=session)

    async def new(self,
                  ticket_id_fk: int,
                  admin_id_fk: int,
                  action_type: ActionType,
                  created_at: datetime = None,
                  details: str = None
                  ) -> AdminAction:
        return await self.session.merge(
            AdminAction(
                ticket_id_fk=ticket_id_fk,
                admin_id=admin_id_fk,
                action_type=action_type,
                created_at=created_at,
                details=details
            )
        )
