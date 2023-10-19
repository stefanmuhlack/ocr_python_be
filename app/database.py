import sqlite3
import logging
from app.config import Config

logger = logging.getLogger(__name__)

def insert_pdf_metadata(filename, upload_date):
    try:
        with sqlite3.connect(Config.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO PDFs (filename, upload_date) VALUES (?, ?)', (filename, upload_date))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
    except Exception as e:
        logger.error(f"Exception in `insert_pdf_metadata`: {e}")

def retrieve_pdf_metadata(filename):
    try:
        with sqlite3.connect(Config.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM PDFs WHERE filename=?', (filename,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")


def update_pdf_metadata(filename, new_upload_date):
    try:
        with sqlite3.connect(Config.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE PDFs SET upload_date=? WHERE filename=?', (new_upload_date, filename))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")


def delete_pdf_metadata(filename):
    try:
        with sqlite3.connect(Config.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM PDFs WHERE filename=?', (filename,))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")