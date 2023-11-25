from datetime import datetime
from uuid import uuid4

from app.libs.helper import generate_link
from .base import db


class PostModel(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(40), nullable=True)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __init__(
        self, title: str, content: str, author=None, date_created=None
    ):
        self.id = uuid4().hex[:8]
        self.title = title.strip()
        self.content = content
        self.author = author
        if date_created:
            self.date_created = datetime.fromisoformat(date_created)

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.get(_id)

    def to_json(self):
        return {
            "id": self.id,
            "link": generate_link(self.title, self.id),
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
