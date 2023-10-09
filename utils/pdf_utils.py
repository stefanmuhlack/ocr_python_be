from pdf2image import convert_from_bytes

def process_pdf(contents: bytes):
    try:
        images = convert_from_bytes(contents)
        return images
    except Exception as e:
        raise e
