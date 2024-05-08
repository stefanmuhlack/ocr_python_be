from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='templates')

