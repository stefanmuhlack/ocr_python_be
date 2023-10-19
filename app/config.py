import os


class Config:
    # Path to the Poppler library (used for PDF processing)
    POPPLER_PATH = os.environ.get('POPPLER_PATH', r"C:\Program Files\Poppler R23.08.0-0\poppler-23.08.0\Library\bin")

    # Path to the SQLite database
    DB_PATH = os.environ.get('DB_PATH', 'ocr_backend.db')

    # Directory to store template files
    TEMPLATES_DIR = os.environ.get('TEMPLATES_DIR', 'templates')