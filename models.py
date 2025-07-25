from app import db
from datetime import datetime
import json


class Bundle(db.Model):
    __tablename__ = 'bundles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    total_pieces = db.Column(db.Integer, nullable=False)
    
    # Store additional expenses as JSON
    additional_expenses = db.Column(db.Text, nullable=False, default='{}')
    
    # Store classification data as JSON
    classification = db.Column(db.Text, nullable=False, default='{}')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Bundle {self.name}>'
    
    def get_additional_expenses(self):
        """Parse additional expenses from JSON"""
        try:
            return json.loads(self.additional_expenses)
        except (json.JSONDecodeError, TypeError):
            return {'transport': 0, 'cleaning': 0, 'other': 0}
    
    def set_additional_expenses(self, expenses_dict):
        """Store additional expenses as JSON"""
        self.additional_expenses = json.dumps(expenses_dict)
    
    def get_classification(self):
        """Parse classification from JSON"""
        try:
            return json.loads(self.classification)
        except (json.JSONDecodeError, TypeError):
            return {
                'by_type': {'hombre': 0, 'mujer': 0, 'ninos': 0, 'hogar': 0},
                'by_quality': {'premium': 0, 'regular': 0, 'economica': 0, 'rechazo': 0}
            }
    
    def set_classification(self, classification_dict):
        """Store classification as JSON"""
        self.classification = json.dumps(classification_dict)
    
    def to_dict(self):
        """Convert to dictionary for compatibility with existing code"""
        return {
            'id': self.id,
            'name': self.name,
            'total_cost': self.total_cost,
            'total_pieces': self.total_pieces,
            'additional_expenses': self.get_additional_expenses(),
            'classification': self.get_classification(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Config(db.Model):
    __tablename__ = 'config'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Config {self.key}>'
    
    @staticmethod
    def get_config():
        """Get complete configuration as dictionary"""
        config_items = Config.query.all()
        config_dict = {}
        
        for item in config_items:
            try:
                config_dict[item.key] = json.loads(item.value)
            except json.JSONDecodeError:
                config_dict[item.key] = item.value
        
        # Set defaults if not found
        if 'profit_percentages' not in config_dict:
            config_dict['profit_percentages'] = {
                'premium': 80,
                'regular': 50,
                'economica': 30,
                'rechazo': 0
            }
        
        if 'default_expenses' not in config_dict:
            config_dict['default_expenses'] = {
                'transport': 0,
                'cleaning': 0,
                'other': 0
            }
        
        return config_dict
    
    @staticmethod
    def set_config(config_dict):
        """Set complete configuration from dictionary"""
        for key, value in config_dict.items():
            config_item = Config.query.filter_by(key=key).first()
            
            if config_item:
                config_item.value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
                config_item.updated_at = datetime.utcnow()
            else:
                config_item = Config(
                    key=key,
                    value=json.dumps(value) if isinstance(value, (dict, list)) else str(value)
                )
                db.session.add(config_item)
        
        db.session.commit()