from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_session
from ..models.template import Template
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/templates")
async def create_template(template_data: Template, db: Session = Depends(get_session)):
    try:
        new_template = Template(**template_data.dict())
        db.add(new_template)
        db.commit()
        return {'message': 'Template created successfully', 'template_id': new_template.id}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create template: {e}")
        raise HTTPException(status_code=500, detail="Unable to create template")

@router.get("/templates/{template_id}")
async def get_template(template_id: int, db: Session = Depends(get_session)):
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.delete("/templates/{template_id}")
async def delete_template(template_id: int, db: Session = Depends(get_session)):
    try:
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        db.delete(template)
        db.commit()
        return {'message': 'Template deleted successfully'}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete template: {e}")
        raise HTTPException(status_code=500, detail="Unable to delete template")
