
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
