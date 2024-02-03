from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from sqlalchemy.orm import relationship
from db import Base, engine

Base.metadata.create_all(bind=engine)


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(200))
    role = Column(String(50))
    is_active = Column(Boolean, default=True)
    token = Column(String(400), default='')

    notifications = relationship('Notifications', back_populates='user')

