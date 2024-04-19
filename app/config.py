import os

class Config:
    # Environment setup
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

    # Path to the Poppler library (used for PDF processing)
    POPPLER_PATH = os.getenv('POPPLER_PATH', r"C:\Program Files\Poppler R23.08.0-0\poppler-23.08.0\Library\bin")

    # Path to the SQLite database
    DB_PATH = os.getenv('DB_PATH', 'ocr_backend.db')

    # Directory to store template files
    TEMPLATES_DIR = os.getenv('TEMPLATES_DIR', 'templates')

    # Ensure all configurations are set properly
    @staticmethod
    def verify_config():
        missing = [var for var in ["ENVIRONMENT", "POPPLER_PATH", "DB_PATH", "TEMPLATES_DIR"] if not getattr(Config, var)]
        if missing:
            raise Exception(f"Missing environment variables: {', '.join(missing)}")

    # Add more configurations dynamically based on the environment
    if ENVIRONMENT == 'production':
        DB_PATH = os.getenv('PROD_DB_PATH', 'prod_ocr_backend.db')
        TEMPLATES_DIR = os.getenv('PROD_TEMPLATES_DIR', 'prod_templates')
    elif ENVIRONMENT == 'staging':
        DB_PATH = os.getenv('STAGING_DB_PATH', 'staging_ocr_backend.db')
        TEMPLATES_DIR = os.getenv('STAGING_TEMPLATES_DIR', 'staging_templates')
