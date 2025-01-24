"""Database class with all-in-one features."""
from sqlalchemy.ext.asyncio import AsyncSession

from .repos import UserRepo, TicketRepo, AdminActionRepo, BanRepo


class Database:
    """Database class.

    is the highest abstraction level of database and
    can be used in the api_handler or any others bot-side repo.
    """

    user: UserRepo
    ticket: TicketRepo
    admin_action: AdminActionRepo
    ban: BanRepo
    """ User repository """

    def __init__(
            self,
            session: AsyncSession,
            user: UserRepo = None,
            ticket: TicketRepo = None,
            admin_action: AdminActionRepo = None,
            ban: BanRepo = None
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        :param user: (Optional) User repository
        """
        self.session = session
        self.user = user or UserRepo(session=session)
        self.ticket = ticket or TicketRepo(session=session)
        self.admin_action = admin_action or AdminActionRepo(session=session)
        self.ban = ban or BanRepo(session=session)
