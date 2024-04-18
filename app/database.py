from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    templates = relationship('Template', back_populates='owner')

class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='templates')

# Setup database session management
Base.metadata.create_all(engine)

def get_session():
    try:
        db_session = SessionLocal()
        return db_session
    except Exception as e:
        print(f'Error creating database session: {e}')
        return None

# Example usage
with get_session() as session:
    user = User(name='John Doe')
    session.add(user)
    session.commit()
    print('User added successfully!')
Base.metadata.create_all(engine)
        logger.error(f"Database error: {e}")
