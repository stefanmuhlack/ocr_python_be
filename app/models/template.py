from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='templates')
    fields = relationship('TemplateField', back_populates='template', cascade='all, delete-orphan')

class TemplateField(Base):
    __tablename__ = 'template_fields'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    field_type = Column(String(50), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id'))
    template = relationship('Template', back_populates='fields')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def validate_coordinates(self):
        if self.x < 0 or self.y < 0:
            raise ValueError("Coordinates must be non-negative")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_coordinates()

