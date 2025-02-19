from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.db import Base
from app.schemas.constants import UserRoleDB



class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(128), unique=True, nullable=False)
    role = Column(Enum(UserRoleDB), default=UserRoleDB.USER, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    files = relationship('File', back_populates='user')

    # TODO: Add relationships to:
    #  - user_auth
    #  - user_details
    #  - support_request
    #  - user_personal_list
    #  - book_rating
    #  - user_bookmark
    #  - books
    #  - author_curators
    #  - publisher_curators

    def __repr__(self):
        return (f"<UserDto("
                f"user_id='{self.user_id}',"
                f" username='{self.username}',"
                f" role='{self.role}',"
                f" created_at='{self.created_at}'"
                f")>")
