from datetime import datetime
from datetime import timedelta

from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Project(Base):
    __tablename__ = "project"

    uuid = Column(
        String(36),
        unique=True,
        primary_key=True,
        nullable=False
    )

    title = Column(
        String(100),
        nullable=False,
    )

    date = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    tag = Column(Text)

    web = Column(
        String(256)
    )
    github = Column(
        String(256)
    )

    a = Column(Text)  # 기획 의도
    b = Column(Text)  # 특징
    c = Column(Text)  # 느낀점

    def __repr__(self):
        return f"<Project uuid={self.uuid!r}, title={self.title!r}>"


class User(Base):
    __tablename__ = "user"

    id = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    email = Column(
        String(96),
        unique=True,
        nullable=False
    )

    password = Column(
        String(128),
        nullable=False
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email!r}>"


class Code(Base):
    __tablename__ = "code"

    id = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("user.id")
    )

    code = Column(
        String(6),
        nullable=False
    )

    ip = Column(
        String(120),
        nullable=False
    )

    creation_date = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    expired_date = Column(
        DateTime,
        nullable=False
    )

    def __repr__(self):
        return f"<Code id={self.id} owner_id={self.owner_id}>"


class Session(Base):
    __tablename__ = "session"

    id = Column(
        Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("user.id")
    )

    ip = Column(
        String(120),
        nullable=False
    )

    creation_date = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    revoked = Column(
        Boolean,
        nullable=False,
        default=False
    )

    def __repr__(self):
        return f"<Code id={self.id} owner_id={self.owner_id}>"
