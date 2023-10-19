import os

class Config:
    HD_SCREEN_SIZE = (1920, 1080)
    POPPLER_PATH = os.environ.get('POPPLER_PATH', r"C:\Program Files\Poppler R23.08.0-0\poppler-23.08.0\Library\bin")
    DB_PATH = os.environ.get('DB_PATH', 'ocr_backend.db')
    TEMPLATES_DIR = os.environ.get('TEMPLATES_DIR', 'templates')