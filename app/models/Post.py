from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.db import Base
from .Vote import Vote


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    post_url = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user = relationship("User")
    comments = relationship("Comment", cascade="all,delete")
    votes = relationship('Vote', cascade='all,delete')

    @hybrid_property
    def vote_count(self):
        return len(self.votes)
