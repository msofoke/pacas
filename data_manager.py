import json
import os
from datetime import datetime
import logging

class DataManager:
    def __init__(self):
        self.data_dir = 'data'
        self.bundles_file = os.path.join(self.data_dir, 'bundles.json')
        self.config_file = os.path.join(self.data_dir, 'config.json')
        self._ensure_data_directory()
        self._initialize_files()
    
    def _ensure_data_directory(self):
        """Crear directorio de datos si no existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _initialize_files(self):
        """Inicializar archivos JSON si no existen"""
        if not os.path.exists(self.bundles_file):
            self._save_json(self.bundles_file, [])
        
        if not os.path.exists(self.config_file):
            default_config = {
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
            self._save_json(self.config_file, default_config)
    
    def _load_json(self, file_path):
        """Cargar datos de archivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading {file_path}: {e}")
            return [] if 'bundles' in file_path else {}
    
    def _save_json(self, file_path, data):
        """Guardar datos en archivo JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logging.error(f"Error saving {file_path}: {e}")
            return False
    
    def get_all_bundles(self):
        """Obtener todas las pacas"""
        bundles = self._load_json(self.bundles_file)
        # Sort by creation date (newest first)
        return sorted(bundles, key=lambda x: x.get('created_at', ''), reverse=True)
    
    def get_bundle(self, bundle_id):
        """Obtener una paca específica por ID"""
        bundles = self._load_json(self.bundles_file)
        for bundle in bundles:
            if bundle.get('id') == bundle_id:
                return bundle
        return None
    
    def save_bundle(self, bundle_data):
        """Guardar una nueva paca"""
        bundles = self._load_json(self.bundles_file)
        
        # Generate new ID
        max_id = max([bundle.get('id', 0) for bundle in bundles] + [0])
        bundle_data['id'] = max_id + 1
        bundle_data['created_at'] = datetime.now().isoformat()
        
        bundles.append(bundle_data)
        
        if self._save_json(self.bundles_file, bundles):
            return bundle_data['id']
        else:
            raise Exception("Error al guardar la paca")
    
    def delete_bundle(self, bundle_id):
        """Eliminar una paca"""
        bundles = self._load_json(self.bundles_file)
        original_length = len(bundles)
        
        bundles = [bundle for bundle in bundles if bundle.get('id') != bundle_id]
        
        if len(bundles) < original_length:
            return self._save_json(self.bundles_file, bundles)
        return False
    
    def get_config(self):
        """Obtener configuración"""
        return self._load_json(self.config_file)
    
    def save_config(self, config_data):
        """Guardar configuración"""
        if not self._save_json(self.config_file, config_data):
            raise Exception("Error al guardar la configuración")
