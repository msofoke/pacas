from models import Bundle, Config, db
from datetime import datetime
import logging


class DataService:
    """Service class to handle data operations with PostgreSQL database"""
    
    @staticmethod
    def get_all_bundles():
        """Get all bundles ordered by creation date (newest first)"""
        try:
            bundles = Bundle.query.order_by(Bundle.created_at.desc()).all()
            return [bundle.to_dict() for bundle in bundles]
        except Exception as e:
            logging.error(f"Error getting all bundles: {e}")
            return []
    
    @staticmethod
    def get_bundle(bundle_id):
        """Get a specific bundle by ID"""
        try:
            bundle = Bundle.query.get(bundle_id)
            return bundle.to_dict() if bundle else None
        except Exception as e:
            logging.error(f"Error getting bundle {bundle_id}: {e}")
            return None
    
    @staticmethod
    def save_bundle(bundle_data):
        """Save a new bundle to the database"""
        try:
            bundle = Bundle(
                name=bundle_data['name'],
                total_cost=bundle_data['total_cost'],
                total_pieces=bundle_data['total_pieces']
            )
            
            bundle.set_additional_expenses(bundle_data['additional_expenses'])
            bundle.set_classification(bundle_data['classification'])
            
            db.session.add(bundle)
            db.session.commit()
            
            return bundle.id
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving bundle: {e}")
            raise Exception("Error al guardar la paca")
    
    @staticmethod
    def update_bundle(bundle_id, bundle_data):
        """Update an existing bundle"""
        try:
            bundle = Bundle.query.get(bundle_id)
            if not bundle:
                return False
            
            bundle.name = bundle_data['name']
            bundle.total_cost = bundle_data['total_cost']
            bundle.total_pieces = bundle_data['total_pieces']
            bundle.updated_at = datetime.utcnow()
            
            bundle.set_additional_expenses(bundle_data['additional_expenses'])
            bundle.set_classification(bundle_data['classification'])
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating bundle {bundle_id}: {e}")
            raise Exception("Error al actualizar la paca")
    
    @staticmethod
    def delete_bundle(bundle_id):
        """Delete a bundle from the database"""
        try:
            bundle = Bundle.query.get(bundle_id)
            if not bundle:
                return False
            
            db.session.delete(bundle)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting bundle {bundle_id}: {e}")
            return False
    
    @staticmethod
    def get_config():
        """Get application configuration"""
        try:
            return Config.get_config()
        except Exception as e:
            logging.error(f"Error getting config: {e}")
            # Return default config
            return {
                'profit_percentages': {
                    'premium': 80,
                    'regular': 50,
                    'economica': 30,
                    'rechazo': 0
                },
                'default_expenses': {
                    'transport': 0,
                    'cleaning': 0,
                    'other': 0
                }
            }
    
    @staticmethod
    def save_config(config_data):
        """Save application configuration"""
        try:
            Config.set_config(config_data)
        except Exception as e:
            logging.error(f"Error saving config: {e}")
            raise Exception("Error al guardar la configuración")