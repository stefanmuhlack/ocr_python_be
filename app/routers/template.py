from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.template import Template, TemplateField
from ..security.auth import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def validate_template_data(template_data):
    """Validate template data before processing."""
    if 'name' not in template_data or not template_data['name']:
        raise HTTPException(status_code=400, detail="Template name is required")
    if 'fields' not in template_data or not isinstance(template_data['fields'], list):
        raise HTTPException(status_code=400, detail="Template fields are required and must be a list")

@router.post("/templates/")
def create_template(template_data: dict, db: Session = Depends(get_db)):
    """Create a new template."""
    try:
        validate_template_data(template_data)
        fields_data = template_data.pop('fields', [])
        new_template = Template(**template_data)
        for field in fields_data:
            new_template.fields.append(TemplateField(**field))
        db.add(new_template)
        db.commit()
        return {'status': 'success', 'message': 'Template created successfully', 'template_id': new_template.id}
    except Exception as e:
        db.rollback()
        logger.error(f'Failed to create template: {e}')
        raise HTTPException(status_code=500, detail='Unable to create template due to server error')

@router.put("/templates/{template_id}")
def update_template(template_id: int, template_data: dict, db: Session = Depends(get_db)):
    """Update an existing template."""
    try:
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        validate_template_data(template_data)
        fields_data = template_data.pop('fields', [])
        for key, value in template_data.items():
            setattr(template, key, value)
        db.query(TemplateField).filter(TemplateField.template_id == template_id).delete()
        for field in fields_data:
            template.fields.append(TemplateField(**field))
        db.commit()
        return {'status': 'success', 'message': 'Template updated successfully'}
    except Exception as e:
        db.rollback()
        logger.error(f'Failed to update template: {e}')
        raise HTTPException(status_code=500, detail='Unable to update template due to server error')

@router.delete("/templates/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    """Delete an existing template."""
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

