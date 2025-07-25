"""
Migration script to move data from JSON files to PostgreSQL database
"""
import json
import os
from datetime import datetime
from app import app, db
from models import Bundle, Config
import logging

def migrate_bundles_from_json():
    """Migrate bundles from JSON file to PostgreSQL"""
    json_file = 'data/bundles.json'
    
    if not os.path.exists(json_file):
        print("No bundles.json file found, skipping bundle migration")
        return
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            bundles_data = json.load(f)
        
        migrated_count = 0
        
        for bundle_data in bundles_data:
            # Check if bundle already exists
            existing_bundle = Bundle.query.filter_by(name=bundle_data['name']).first()
            if existing_bundle:
                print(f"Bundle '{bundle_data['name']}' already exists, skipping")
                continue
            
            # Create new bundle
            bundle = Bundle(
                name=bundle_data['name'],
                total_cost=bundle_data['total_cost'],
                total_pieces=bundle_data['total_pieces']
            )
            
            # Set additional expenses and classification
            bundle.set_additional_expenses(bundle_data.get('additional_expenses', {}))
            bundle.set_classification(bundle_data.get('classification', {}))
            
            # Set creation date if available
            if 'created_at' in bundle_data:
                try:
                    bundle.created_at = datetime.fromisoformat(bundle_data['created_at'].replace('Z', '+00:00'))
                except:
                    bundle.created_at = datetime.utcnow()
            
            db.session.add(bundle)
            migrated_count += 1
        
        db.session.commit()
        print(f"Successfully migrated {migrated_count} bundles from JSON to PostgreSQL")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error migrating bundles: {e}")
        raise

def migrate_config_from_json():
    """Migrate configuration from JSON file to PostgreSQL"""
    json_file = 'data/config.json'
    
    if not os.path.exists(json_file):
        print("No config.json file found, skipping config migration")
        return
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Clear existing config
        Config.query.delete()
        
        # Add new config
        for key, value in config_data.items():
            config_item = Config(
                key=key,
                value=json.dumps(value) if isinstance(value, (dict, list)) else str(value)
            )
            db.session.add(config_item)
        
        db.session.commit()
        print("Successfully migrated configuration from JSON to PostgreSQL")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error migrating config: {e}")
        raise

def backup_json_files():
    """Create backup of JSON files before migration"""
    data_dir = 'data'
    backup_dir = 'data_backup'
    
    if not os.path.exists(data_dir):
        return
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copy JSON files
    for filename in ['bundles.json', 'config.json']:
        source_path = os.path.join(data_dir, filename)
        if os.path.exists(source_path):
            backup_path = os.path.join(backup_dir, f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            import shutil
            shutil.copy2(source_path, backup_path)
            print(f"Backed up {filename} to {backup_path}")

def main():
    """Main migration function"""
    print("Starting data migration from JSON to PostgreSQL...")
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Backup JSON files first
        backup_json_files()
        
        # Migrate data
        migrate_config_from_json()
        migrate_bundles_from_json()
        
        print("Data migration completed successfully!")

if __name__ == '__main__':
    main()