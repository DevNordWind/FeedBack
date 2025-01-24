"""Repository file."""
import abc
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import delete, select, exists, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base

AbstractModel = TypeVar('AbstractModel')


class Repository(Generic[AbstractModel]):
    """Repository abstract class."""

    type_model: type[Base]
    session: AsyncSession

    def __init__(self, type_model: type[Base], session: AsyncSession):
        """Initialize abstract repository class.

        :param type_model: Which model will be used for operations
        :param session: Session in which repository will work.
        """
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel:
        """Get an ONE model from the database with PK.

        :param ident: Key which need to find entry in database
        :return:
        """
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, whereclause) -> AbstractModel | None:
        """Get an ONE model from the database with whereclause.

        :param whereclause: Clause by which entry will be found
        :return: Model if only one model was found, else None.
        """
        statement = select(self.type_model).where(whereclause)
        return await self.session.scalar(statement)

    async def get_many(
            self, whereclause, limit: int = 100, order_by=None
    ) -> Sequence[AbstractModel]:
        """Get many models from the database with whereclause.

        :param whereclause: Where clause for finding models
        :param limit: (Optional) Limit count of results
        :param order_by: (Optional) Order by clause.

        Example:
        >> Repository.get_many(Model.id == 1, limit=10, order_by=Model.id)

        :return: List of founded models
        """
        statement = select(self.type_model).where(whereclause).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def is_exists(self, whereclause) -> bool:
        stmt = select(exists().where(whereclause))
        return await self.session.scalar(stmt)

    async def update(self, whereclause, values: dict):
        stmt = update(self.type_model).where(whereclause).values(**values)
        await self.session.execute(stmt)

    async def count(self, whereclause=None) -> int:
        stmt = select(func.count(self.type_model.id))
        if whereclause is not None:
            stmt = select(func.count(self.type_model.id)).where(whereclause)
            return await self.session.scalar(stmt)
        return await self.session.scalar(stmt)

    async def delete(self, whereclause) -> None:
        """Delete model from the database.

        :param whereclause: (Optional) Which statement
        :return: Nothing
        """
        statement = delete(self.type_model).where(whereclause)
        await self.session.execute(statement)

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None:
        """Add new entry of model to the database.

        :return: Nothing.
        """
        ...
