import sqlite3
from datetime import datetime

# Initialize SQLite database
conn = sqlite3.connect('ocr_backend.db')
cursor = conn.cursor()

# Create PDFs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS PDFs (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    upload_date TEXT NOT NULL
)
''')

# Create Templates table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Templates (
    id INTEGER PRIMARY KEY,
    pdf_id INTEGER,
    page_number INTEGER,
    rectangle_info TEXT,
    FOREIGN KEY (pdf_id) REFERENCES PDFs (id)
)
''')

# Create OCR_Results table
cursor.execute('''
CREATE TABLE IF NOT EXISTS OCR_Results (
    id INTEGER PRIMARY KEY,
    pdf_id INTEGER,
    ocr_text TEXT,
    processed_date TEXT NOT NULL,
    FOREIGN KEY (pdf_id) REFERENCES PDFs (id)
)
''')

conn.commit()
conn.close()

print('Database initialized and tables created.')