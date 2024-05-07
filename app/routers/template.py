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

