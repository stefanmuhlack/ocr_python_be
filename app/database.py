import sqlite3

DB_PATH = 'ocr_backend.db'

def insert_pdf_metadata(filename, upload_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO PDFs (filename, upload_date) VALUES (?, ?)', (filename, upload_date))
    conn.commit()
    conn.close()

# Add more database functions as needed...
