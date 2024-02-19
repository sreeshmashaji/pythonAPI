from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey,Integer, String, text
from .database import Base
from sqlalchemy.orm import relationship

class Votes(Base):
    __tablename__='votes'
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)

class Users(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    phoneNumber=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Post(Base):
    __tablename__='posts'
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,nullable=False,server_default='TRUE')
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("Users")




    



