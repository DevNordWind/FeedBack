from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..enums import TicketStatus
from ..models.ticket import Ticket


class TicketRepo(Repository[Ticket]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=Ticket, session=session)

    async def new(self,
                  user_id_fk: int,
                  question: str,
                  status: TicketStatus = TicketStatus.PENDING
                  ) -> Ticket:
        return await self.session.merge(
            Ticket(
                user_id_fk=user_id_fk,
                question=question,
                status=status
            )
        )
