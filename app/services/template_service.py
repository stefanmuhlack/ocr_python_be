import logging
from sqlalchemy.orm import Session
from ..models.template import Template, TemplateField

class TemplateService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def create_template(self, template_data):
        try:
            fields_data = template_data.pop('fields', [])
            new_template = Template(**template_data)
            for field in fields_data:
                new_template.fields.append(TemplateField(**field))
            self.db.add(new_template)
            self.db.commit()
            return new_template
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error creating template: {e}")
            raise e

    def update_template(self, template_id, template_data):
        try:
            template = self.db.query(Template).filter(Template.id == template_id).first()
            if not template:
                return None
            fields_data = template_data.pop('fields', [])
            for key, value in template_data.items():
                setattr(template, key, value)
            self.db.query(TemplateField).filter(TemplateField.template_id == template_id).delete()
            for field in fields_data:
                template.fields.append(TemplateField(**field))
            self.db.commit()
            return template
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error updating template: {e}")
            raise e

    def delete_template(self, template_id):
        try:
            template = self.db.query(Template).filter(Template.id == template_id).first()
            if not template:
                return None
            self.db.delete(template)
            self.db.commit()
            return template
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error deleting template: {e}")
            raise e

