from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, func
from app.db import Base
from app.schemas.constants import UserRoleDB


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(128), unique=True, nullable=False)
    role = Column(Enum(UserRoleDB), default=UserRoleDB.user, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # TODO: Add relationships


    def __repr__(self):
        return (f"<UserDto("
                f"user_id='{self.user_id}',"
                f" username='{self.username}',"
                f" role='{self.role}',"
                f" created_at='{self.created_at}'"
                f")>")
