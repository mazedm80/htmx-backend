from sqlalchemy.orm import DeclarativeBase

from core.database.postgres import PSQLHandler


class Base(DeclarativeBase):
    """Base class for all the models"""

    pass
