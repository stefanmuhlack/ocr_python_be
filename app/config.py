import os

class Config:
    HD_SCREEN_SIZE = (1920, 1080)
    POPPLER_PATH = os.environ.get('POPPLER_PATH', default_path)  # default_path can be the current hardcoded path or another fallback.
