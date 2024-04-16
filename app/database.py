from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from app.config import Config

Base = declarative_base()

class PDFMetadata(Base):
    __tablename__ = 'PDFs'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)

# Setup the database connection and scoped session
engine = create_engine(f'sqlite:///{Config.DB_PATH}', connect_args={"check_same_thread": False})
Session = scoped_session(sessionmaker(bind=engine))

def insert_pdf_metadata(filename, upload_date):
    session = Session()
    new_pdf = PDFMetadata(filename=filename, upload_date=upload_date)
    session.add(new_pdf)
    session.commit()
    session.close()

def retrieve_pdf_metadata(filename):
    session = Session()
    pdf_metadata = session.query(PDFMetadata).filter(PDFMetadata.filename == filename).first()
    session.close()
    return pdf_metadata

def update_pdf_metadata(filename, new_upload_date):
    session = Session()
    pdf_metadata = session.query(PDFMetadata).filter(PDFMetadata.filename == filename).first()
    if pdf_metadata:
        pdf_metadata.upload_date = new_upload_date
        session.commit()
    session.close()

def delete_pdf_metadata(filename):
    session = Session()
    pdf_metadata = session.query(PDFMetadata).filter(PDFMetadata.filename == filename).first()
    if pdf_metadata:
        session.delete(pdf_metadata)
        session.commit()
    session.close()

# Create all tables in the database which are defined by Base's subclasses such as PDFMetadata
Base.metadata.create_all(engine)

Base.metadata.create_all(engine)
        logger.error(f"Database error: {e}")
