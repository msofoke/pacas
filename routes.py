from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app
from data_service import DataService
from utils import calculate_bundle_metrics
import logging

@app.route('/')
def index():
    """Dashboard principal"""
    try:
        bundles = DataService.get_all_bundles()
        config = DataService.get_config()
        
        # Calculate summary statistics
        total_bundles = len(bundles)
        total_investment = sum(bundle.get('total_cost', 0) for bundle in bundles)
        total_estimated_profit = 0
        
        for bundle in bundles:
            metrics = calculate_bundle_metrics(bundle, config)
            total_estimated_profit += metrics.get('total_estimated_profit', 0)
        
        summary = {
            'total_bundles': total_bundles,
            'total_investment': total_investment,
            'total_estimated_profit': total_estimated_profit,
            'estimated_profit_margin': (total_estimated_profit / total_investment * 100) if total_investment > 0 else 0
        }
        
        return render_template('index.html', bundles=bundles, summary=summary)
    except Exception as e:
        logging.error(f"Error in index route: {e}")
        flash('Error al cargar los datos', 'error')
        return render_template('index.html', bundles=[], summary={})

@app.route('/config', methods=['GET', 'POST'])
def config():
    """Configuración de porcentajes de ganancia"""
    if request.method == 'POST':
        try:
            config_data = {
                'profit_percentages': {
                    'premium': float(request.form.get('premium', 80)),
                    'regular': float(request.form.get('regular', 50)),
                    'economica': float(request.form.get('economica', 30)),
                    'rechazo': float(request.form.get('rechazo', 0))
                },
                'default_expenses': {
                    'transport': float(request.form.get('transport', 0)),
                    'cleaning': float(request.form.get('cleaning', 0)),
                    'other': float(request.form.get('other', 0))
                }
            }
            
            DataService.save_config(config_data)
            flash('Configuración guardada exitosamente', 'success')
            return redirect(url_for('config'))
        except ValueError as e:
            flash('Error: Valores numéricos inválidos', 'error')
        except Exception as e:
            logging.error(f"Error saving config: {e}")
            flash('Error al guardar la configuración', 'error')
    
    config_data = DataService.get_config()
    return render_template('config.html', config=config_data)

@app.route('/new_bundle', methods=['GET', 'POST'])
def new_bundle():
    """Crear nueva paca"""
    if request.method == 'POST':
        try:
            # Get basic bundle data
            bundle_data = {
                'name': request.form.get('name', '').strip(),
                'total_cost': float(request.form.get('total_cost', 0)),
                'total_pieces': int(request.form.get('total_pieces', 0)),
                'additional_expenses': {
                    'transport': float(request.form.get('transport', 0)),
                    'cleaning': float(request.form.get('cleaning', 0)),
                    'other': float(request.form.get('other', 0))
                },
                'classification': {
                    'by_type': {
                        'hombre': int(request.form.get('hombre', 0)),
                        'mujer': int(request.form.get('mujer', 0)),
                        'ninos': int(request.form.get('ninos', 0)),
                        'hogar': int(request.form.get('hogar', 0))
                    },
                    'by_quality': {
                        'premium': int(request.form.get('premium', 0)),
                        'regular': int(request.form.get('regular', 0)),
                        'economica': int(request.form.get('economica', 0)),
                        'rechazo': int(request.form.get('rechazo', 0))
                    }
                }
            }
            
            # Validate data
            if not bundle_data['name']:
                flash('El nombre de la paca es requerido', 'error')
                return render_template('new_bundle.html')
            
            if bundle_data['total_cost'] <= 0:
                flash('El costo total debe ser mayor a 0', 'error')
                return render_template('new_bundle.html')
            
            if bundle_data['total_pieces'] <= 0:
                flash('El número de piezas debe ser mayor a 0', 'error')
                return render_template('new_bundle.html')
            
            # Validate classification totals
            total_by_type = sum(bundle_data['classification']['by_type'].values())
            total_by_quality = sum(bundle_data['classification']['by_quality'].values())
            
            if total_by_type != bundle_data['total_pieces']:
                flash(f'La suma de piezas por tipo ({total_by_type}) debe ser igual al total de piezas ({bundle_data["total_pieces"]})', 'error')
                return render_template('new_bundle.html')
            
            if total_by_quality != bundle_data['total_pieces']:
                flash(f'La suma de piezas por calidad ({total_by_quality}) debe ser igual al total de piezas ({bundle_data["total_pieces"]})', 'error')
                return render_template('new_bundle.html')
            
            # Save bundle
            bundle_id = DataService.save_bundle(bundle_data)
            flash('Paca creada exitosamente', 'success')
            return redirect(url_for('bundle_details', bundle_id=bundle_id))
            
        except ValueError as e:
            flash('Error: Valores numéricos inválidos', 'error')
        except Exception as e:
            logging.error(f"Error creating bundle: {e}")
            flash('Error al crear la paca', 'error')
    
    # Get default expenses from config
    config = DataService.get_config()
    default_expenses = config.get('default_expenses', {})
    
    return render_template('new_bundle.html', default_expenses=default_expenses)

@app.route('/bundle/<int:bundle_id>')
def bundle_details(bundle_id):
    """Detalles de una paca específica"""
    try:
        bundle = DataService.get_bundle(bundle_id)
        if not bundle:
            flash('Paca no encontrada', 'error')
            return redirect(url_for('index'))
        
        config = DataService.get_config()
        metrics = calculate_bundle_metrics(bundle, config)
        
        return render_template('bundle_details.html', bundle=bundle, metrics=metrics)
    except Exception as e:
        logging.error(f"Error loading bundle details: {e}")
        flash('Error al cargar los detalles de la paca', 'error')
        return redirect(url_for('index'))

@app.route('/delete_bundle/<int:bundle_id>', methods=['POST'])
def delete_bundle(bundle_id):
    """Eliminar una paca"""
    try:
        if DataService.delete_bundle(bundle_id):
            flash('Paca eliminada exitosamente', 'success')
        else:
            flash('Paca no encontrada', 'error')
    except Exception as e:
        logging.error(f"Error deleting bundle: {e}")
        flash('Error al eliminar la paca', 'error')
    
    return redirect(url_for('index'))

@app.route('/edit_bundle/<int:bundle_id>', methods=['GET', 'POST'])
def edit_bundle(bundle_id):
    """Editar una paca existente"""
    bundle = DataService.get_bundle(bundle_id)
    if not bundle:
        flash('Paca no encontrada', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            # Get updated bundle data
            bundle_data = {
                'name': request.form.get('name', '').strip(),
                'total_cost': float(request.form.get('total_cost', 0)),
                'total_pieces': int(request.form.get('total_pieces', 0)),
                'additional_expenses': {
                    'transport': float(request.form.get('transport', 0)),
                    'cleaning': float(request.form.get('cleaning', 0)),
                    'other': float(request.form.get('other', 0))
                },
                'classification': {
                    'by_type': {
                        'hombre': int(request.form.get('hombre', 0)),
                        'mujer': int(request.form.get('mujer', 0)),
                        'ninos': int(request.form.get('ninos', 0)),
                        'hogar': int(request.form.get('hogar', 0))
                    },
                    'by_quality': {
                        'premium': int(request.form.get('premium', 0)),
                        'regular': int(request.form.get('regular', 0)),
                        'economica': int(request.form.get('economica', 0)),
                        'rechazo': int(request.form.get('rechazo', 0))
                    }
                }
            }
            
            # Validate data
            if not bundle_data['name']:
                flash('El nombre de la paca es requerido', 'error')
                return render_template('edit_bundle.html', bundle=bundle)
            
            if bundle_data['total_cost'] <= 0:
                flash('El costo total debe ser mayor a 0', 'error')
                return render_template('edit_bundle.html', bundle=bundle)
            
            if bundle_data['total_pieces'] <= 0:
                flash('El número de piezas debe ser mayor a 0', 'error')
                return render_template('edit_bundle.html', bundle=bundle)
            
            # Validate classification totals
            total_by_type = sum(bundle_data['classification']['by_type'].values())
            total_by_quality = sum(bundle_data['classification']['by_quality'].values())
            
            if total_by_type != bundle_data['total_pieces']:
                flash(f'La suma de piezas por tipo ({total_by_type}) debe ser igual al total de piezas ({bundle_data["total_pieces"]})', 'error')
                return render_template('edit_bundle.html', bundle=bundle)
            
            if total_by_quality != bundle_data['total_pieces']:
                flash(f'La suma de piezas por calidad ({total_by_quality}) debe ser igual al total de piezas ({bundle_data["total_pieces"]})', 'error')
                return render_template('edit_bundle.html', bundle=bundle)
            
            # Update bundle
            if DataService.update_bundle(bundle_id, bundle_data):
                flash('Paca actualizada exitosamente', 'success')
                return redirect(url_for('bundle_details', bundle_id=bundle_id))
            else:
                flash('Error al actualizar la paca', 'error')
                
        except ValueError as e:
            flash('Error: Valores numéricos inválidos', 'error')
        except Exception as e:
            logging.error(f"Error updating bundle: {e}")
            flash('Error al actualizar la paca', 'error')
    
    return render_template('edit_bundle.html', bundle=bundle)
