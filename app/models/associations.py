from .base import db

post_x_tag = db.Table(
    "post_x_tag",
    db.metadata,
    db.Column("post_id", db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.ForeignKey("tags.id"), primary_key=True),
)
