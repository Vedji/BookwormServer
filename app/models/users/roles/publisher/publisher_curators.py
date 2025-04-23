from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from datetime import datetime
from app.db import Base
from app.schemas.constants.ticket_attributes import RequestStatus, SupportRequestTypes

if TYPE_CHECKING:
    from ...user import User
    from . import Publishers


class PublisherCurators(Base):
    """
    Таблица ассоциаций кураторов издательств.
    """

    __tablename__ = "publisher_curators"

    publisher_curator_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Уникальный идентификатор куратора.")
    account_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False, comment="Идентификатор курирующего пользователя.")
    publisher_id: Mapped[int] = mapped_column(
        ForeignKey("publishers.publisher_id"), nullable=False, comment="Идентификатор издательства.")

    user: Mapped["User"] = relationship(
        lazy="selectin", back_populates="publisher_curator", uselist=False
    )
    publisher: Mapped["Publishers"] = relationship(
        lazy="selectin", back_populates="publisher_curators", uselist=False
    )

    def __repr__(self):
        return (f"<models.users.roles.publisher.PublisherCurators("
                f"publisher_curator_id='{self.publisher_curator_id}', "
                f"account_id='{self.account_id}', "
                f"publisher_id='{self.publisher_id}')>")
