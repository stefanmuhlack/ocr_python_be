import pytest
from app.ocr_processing import process_image

@pytest.mark.parametrize("image_path, expected_text", [
    ("tests/fixtures/sample_image.png", "Expected OCR Result"),
    ("tests/fixtures/another_sample_image.jpg", "Another Expected Result")
])
def test_ocr_processing(image_path, expected_text):
    # Test OCR processing on sample images
    result = process_image(image_path)
    assert expected_text in result, f"OCR result does not match expected text for {image_path}"
