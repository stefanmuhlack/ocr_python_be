import os
from fastapi import UploadFile, HTTPException
from PIL import Image
from pdf2image import convert_from_path

class PDFService:
    @staticmethod
    def save_uploaded_file(upload_file: UploadFile, target_dir: str) -> str:
        file_location = os.path.join(target_dir, upload_file.filename)
        with open(file_location, 'wb') as f:
            f.write(upload_file.file.read())
        return file_location

    @staticmethod
    def convert_pdf_to_images(pdf_path: str) -> [Image]:
        # Convert PDF file to images
        images = convert_from_path(pdf_path)
        return images
