from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, engine

Base.metadata.create_all(bind=engine)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(200))
    role = Column(String(50))
    is_active = Column(Boolean, default=True)
    token = Column(String(400), default='')

    notifications = relationship('Notifications', back_populates='user')


class Notifications(Base):
    __tablename__ = "Notifications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), default='')
    body = Column(String(255), default='')
    user_id = Column(Integer, ForeignKey('users.id'), default=0)

    user = relationship('Users', back_populates='notifications')
