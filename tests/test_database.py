import pytest
from sqlalchemy.orm import sessionmaker
from app.database import Base, engine

SessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    # Create a session for testing, bind it to an in-memory database
    Base.metadata.create_all(engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(engine)

def test_template_creation(db_session):
    # Test creating and retrieving a template
    from app.models.template import Template
    new_template = Template(name='Test Template', description='A test template.')
    db_session.add(new_template)
    db_session.commit()
    retrieved_template = db_session.query(Template).filter(Template.name == 'Test Template').first()
    assert retrieved_template is not None
    assert retrieved_template.name == 'Test Template'
