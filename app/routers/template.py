from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.template import Template
from ..security.auth import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/template")
async def create_template(template_data: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        new_template = Template(**template_data)
        db.add(new_template)
        db.commit()
        return {'status': 'success', 'message': 'Template created successfully', 'template_id': new_template.id}
    except Exception as e:
        db.rollback()
        logger.error(f'Failed to create template: {e}')
        raise HTTPException(status_code=500, detail='Unable to create template due to server error')

@router.put("/template/{template_id}")
async def update_template(template_id: int, template_data: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        for key, value in template_data.items():
            setattr(template, key, value)
        db.commit()
        return {'status': 'success', 'message': 'Template updated successfully'}
    except Exception as e:
        db.rollback()
        logger.error(f'Failed to update template: {e}')
        raise HTTPException(status_code=500, detail='Unable to update template due to server error')

@router.delete("/template/{template_id}")
async def delete_template(template_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        db.delete(template)
        db.commit()
        return {'status': 'success', 'message': 'Template deleted successfully'}
    except Exception as e:
        db.rollback()
        logger.error(f'Failed to delete template: {e}')
        raise HTTPException(status_code=500, detail='Unable to delete template due to server error')

