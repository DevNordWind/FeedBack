from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import select, func, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import join

from .abstract import Repository
from ..enums import Role
from ..models import User
from ..models.ticket import Ticket


class UserRepo(Repository[User]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=User, session=session)

    async def new(self,
                  user_id: int,
                  first_name: str,
                  role: Role,
                  username: str | None = None,
                  last_name: str | None = None,
                  is_banned: bool | None = None,
                  reg_time: datetime | None = None
                  ) -> User:
        return await self.session.merge(
            User(
                user_id=user_id,
                first_name=first_name,
                role=role,
                username=username,
                last_name=last_name,
                is_banned=is_banned,
                reg_time=reg_time
            )
        )

    async def count_all(self) -> int:
        stmt = select(func.count(User.id))
        return await self.session.scalar(stmt)

    async def get_user_profile(self, id: int) -> Sequence[Row[tuple[Any, Any]]]:
        stmt = select(User.reg_time, func.count(Ticket.id)).outerjoin(Ticket, Ticket.user_id_fk == User.id).where(
            User.id == id).group_by(User.reg_time)
        return (await self.session.execute(stmt)).all()
