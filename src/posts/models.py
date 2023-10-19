from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('user.id'))
    
    author = relationship('User', back_populates='posts')
    likes = relationship('Like', back_populates='post')

class Like(Base):
    __tablename__ = 'like'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    user = relationship('User')
    post = relationship('Post', back_populates='likes')
    
    __table_args__ = (
        UniqueConstraint(
            'post_id', 'user_id'
            ),
        )

    

