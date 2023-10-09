from app.database import engine, metadata

metadata.create_all(engine)
