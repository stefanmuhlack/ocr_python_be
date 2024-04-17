import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from services.ocr_service import OCRService
from services.pdf_service import PDFService

# Setup advanced logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[RotatingFileHandler("app_logs.log", maxBytes=1000000, backupCount=3)])
logger = logging.getLogger(__name__)

app = FastAPI()

# Security contexts
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Include OCR and PDF service routers
app.include_router(OCRService.router, prefix="/ocr", tags=["OCR Operations"])
app.include_router(PDFService.router, prefix="/pdf", tags=["PDF Management"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")
class OCRRequest(BaseModel):
    template_name: str
    rectangles: list

# Include routers
app.include_router(PDFService.router, prefix="/pdf", tags=["pdf"])
app.include_router(OCRService.router, prefix="/template", tags=["template"])

# Separate OCR and PDF handling in respective services for better modularity
