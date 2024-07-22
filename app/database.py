import logging
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from alembic import context

logger = logging.getLogger(__name__)

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

# Alembic Configuration to handle migrations
alembic_cfg = context.config

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = alembic_cfg.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine.connect()
    context.configure(connection=connectable, target_metadata=Base.metadata)
    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connectable.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

def get_session():
    """Get a new database session."""
    try:
        db_session = SessionLocal()
        return db_session
    except Exception as e:
        logger.error(f'Error creating database session: {e}')
        return None

