from datetime import timedelta

from sqlalchemy import func

from app import db


class Project(db.Model):
    uuid = db.Column(
        db.String(36),
        unique=True,
        primary_key=True,
        nullable=False
    )

    title = db.Column(
        db.String(100),
        nullable=False,
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    tag = db.Column(db.Text)

    web = db.Column(
        db.String(256)
    )
    github = db.Column(
        db.String(256)
    )

    a = db.Column(db.Text)  # 기획 의도
    b = db.Column(db.Text)  # 특징
    c = db.Column(db.Text)  # 느낀점

    def __repr__(self):
        return f"<Project uuid={self.uuid!r}, title={self.title!r}>"


class User(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    email = db.Column(
        db.String(96),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(128),
        nullable=False
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email!r}>"


class Code(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    code = db.Column(
        db.String(6),
        nullable=False
    )

    ip = db.Column(
        db.String(120),
        nullable=False
    )

    used = db.Column(
        db.Boolean,
        nullable=False,
    )

    creation_date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "code": self.code if len(self.code) == 1 else "******",
            "ip": self.ip,
            "used": self.used,
            "creation_date": round(self.creation_date.timestamp()),
            "dead_date": round((self.creation_date + timedelta(minutes=3)).timestamp()),
        }

    def __repr__(self):
        return f"<Code id={self.id} owner_id={self.owner_id}>"
