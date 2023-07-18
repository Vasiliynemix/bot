from sqlalchemy import ForeignKey, Column, Table

from .base import Base

PostChannel = Table(
    "post_channels",
    Base.metadata,
    Column("post", ForeignKey("posts.id"), primary_key=True),
    Column("channel", ForeignKey("channels.id"), primary_key=True),
)
