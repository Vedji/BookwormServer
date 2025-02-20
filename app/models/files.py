from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, TIMESTAMP, UniqueConstraint,
    func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.db import Base
from app.schemas.constants import AllowedFileFormats, FileStatus


class File(Base):
    __tablename__ = 'files'

    file_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    file_key = Column(String(255), nullable=False, unique=True)
    mime_type = Column(Enum(AllowedFileFormats), nullable=False, default="application/octet-stream")

    status = Column(Enum(FileStatus), nullable=False, default=FileStatus.EXPIRED)
    bucket_name = Column(String(64), nullable=True)
    s3_url = Column(String(512), nullable=True)
    expires_at = Column(TIMESTAMP, nullable=True)

    uploaded_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    added_user = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    user = relationship('User', back_populates='files')

    # TODO: Add relationships to:
    #  - Books (ref: < book_content, ref: < book_title_image)
    #  - User details (ref: < users_avatar)

    __table_args__ = (
        UniqueConstraint('file_key', name='uq_file_key'),
    )

    def __repr__(self):
        return f"<FileDto(file_id='{self.file_id}', status='{self.status}', file_key='{self.file_key}')>"