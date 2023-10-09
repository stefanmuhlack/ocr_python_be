from app.models.template import OCRRequest
from fastapi import APIRouter

router = APIRouter()

@router.post("/process_ocr/")
async def process_ocr(request: OCRRequest):
    template_name = request.template_name
    page = request.page
    rectangles = request.rectangles
    description = request.description
    classifier = request.classifier
    value_length = request.value_length

    # Process the data, for example, save it to a file
    # You can use the fields here

    return {"message": "Data processed successfully!"}
