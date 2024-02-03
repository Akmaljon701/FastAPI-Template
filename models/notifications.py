from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, engine

Base.metadata.create_all(bind=engine)


class Notifications(Base):
    __tablename__ = "Notifications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), default='')
    body = Column(String(255), default='')
    user_id = Column(Integer, ForeignKey('Users.id'), default=0)

    user = relationship('Users', back_populates='notifications')
