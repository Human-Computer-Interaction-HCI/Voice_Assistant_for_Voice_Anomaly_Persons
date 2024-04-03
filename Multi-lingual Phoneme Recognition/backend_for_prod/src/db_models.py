from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from database import Base
except ImportError:
    from .database import Base


class User(Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(String, primary_key=True)
    password: Mapped[str] = mapped_column(String)

    datasets: Mapped[list["UserDataset"]] = relationship(back_populates="user")
    models: Mapped[list["UserModel"]] = relationship(back_populates="user")


class UserDataset(Base):
    __tablename__ = "user_dataset"

    dataset_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.login"))
    label: Mapped[str] = mapped_column(String, default="default")

    user: Mapped[User] = relationship(back_populates="datasets")
    recordings: Mapped[list["UserRecording"]] = relationship(back_populates="dataset")


class UserRecording(Base):
    __tablename__ = "user_recording"

    recording_id: Mapped[str] = mapped_column(String, primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("user_dataset.dataset_id"))
    label: Mapped[str | None] = mapped_column(String, default=None, nullable=True)

    dataset: Mapped[UserDataset] = relationship(back_populates="recordings")


class UserModel(Base):
    __tablename__ = "user_model"

    model_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("user_dataset.dataset_id"))
    label: Mapped[str | None] = mapped_column(String, default=None, nullable=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.login"))

    user: Mapped[User] = relationship(back_populates="models")
