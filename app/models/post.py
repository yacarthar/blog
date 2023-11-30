from datetime import datetime
from uuid import uuid4

from app.libs.helper import generate_link

from .associations import post_x_tag
from .base import db


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(140), nullable=True)
    author = db.Column(db.String(40), nullable=True)
    toc = db.Column(db.Text, nullable=True)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    category = db.relationship("Category", back_populates="posts")
    tags = db.relationship("Tag", secondary=post_x_tag, back_populates="posts")

    def __init__(
        self,
        title: str,
        content: str,
        author=None,
        summary=None,
        toc=None,
        date_created=None,
    ):
        self.id = uuid4().hex[:8]
        self.title = title.strip()
        self.content = content
        self.author = author
        if date_created:
            self.date_created = datetime.fromisoformat(date_created)
        self.summary = summary
        self.toc = toc

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
            "toc": self.toc[:short] if self.toc is not None else None,
            "tags": [t.name for t in self.tags],
            "category": self.category.name if self.category_id else None,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def refresh(self):
        db.session.refresh(self)
