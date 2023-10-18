import sqlite3

DB_PATH = 'ocr_backend.db'

def insert_pdf_metadata(filename, upload_date):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO PDFs (filename, upload_date) VALUES (?, ?)', (filename, upload_date))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in `insert_pdf_metadata`: {e}")
