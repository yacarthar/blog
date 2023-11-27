from datetime import datetime
from uuid import uuid4

from app.libs.helper import generate_link

from .base import db

association_table = db.Table(
    "associations",
    db.metadata,
    db.Column("post_id", db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.ForeignKey("tags.id"), primary_key=True),
)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(140), nullable=True)
    author = db.Column(db.String(40), nullable=True)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    tags = db.relationship(
        "Tag", secondary=association_table, back_populates="posts"
    )

    def __init__(
        self,
        title: str,
        content: str,
        author=None,
        summary=None,
        date_created=None,
    ):
        self.id = uuid4().hex[:8]
        self.title = title.strip()
        self.content = content
        self.author = author
        if date_created:
            self.date_created = datetime.fromisoformat(date_created)
        self.summary = summary

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.get(_id)

    @property
    def link(self):
        return generate_link(self.title.lower(), self.id)

    def to_json(self, short=None):
        return {
            "id": self.id,
            "link": self.link,
            "title": self.title,
            "content": self.content[:short],
            "author": self.author,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": self.summary,
            "tags": [t.name for t in self.tags],
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def refresh(self):
        db.session.refresh(self)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship(
        "Post", secondary=association_table, back_populates="tags"
    )

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def refresh(self):
        db.session.refresh(self)
