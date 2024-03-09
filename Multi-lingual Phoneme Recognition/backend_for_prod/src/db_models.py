from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column

try:
    from database import Base
except ImportError:
    from .database import Base


class User(Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(String, primary_key=True)
    password: Mapped[str] = mapped_column(String)
