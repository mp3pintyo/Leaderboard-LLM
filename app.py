"""
Flask application for LLM Leaderboard.
Provides API endpoints and web interface for comparing LLM results.
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
import json
from typing import Dict, List, Any, Optional
import tempfile

from database import DatabaseManager
from config import SECRET_KEY, DEBUG, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH, TASK_GROUPS, MODELS
from scripts.import_excel import ExcelImporter


def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    
    # Initialize database manager
    db = DatabaseManager()
    
    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed."""
        if '.' not in filename:
            return False
        file_ext = '.' + filename.rsplit('.', 1)[1].lower()
        return file_ext in ALLOWED_EXTENSIONS
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Web interface routes
    @app.route('/')
    def index():
        """Main leaderboard page."""
        # Get filter parameters from query string
        filters = {}
        
        # Boolean filters
        for param in ['open_source', 'reasoning', 'image_input']:
            value = request.args.get(param)
            if value and value.lower() in ['true', 'false']:
                filters[param] = value.lower() == 'true'
        
        # String filters
        for param in ['tag', 'task_group', 'language', 'sort_by', 'provider']:
            value = request.args.get(param)
            if value:
                filters[param] = value
        
        # Numeric range filters
        numeric_ranges = ['parameters', 'context', 'tokens']
        for param in numeric_ranges:
            min_val = request.args.get(f'min_{param}')
            max_val = request.args.get(f'max_{param}')
            if min_val:
                try:
                    filters[f'min_{param}'] = int(min_val)
                except ValueError:
                    pass
            if max_val:
                try:
                    filters[f'max_{param}'] = int(max_val)
                except ValueError:
                    pass
        
        # Date range filters
        for param in ['date']:
            min_val = request.args.get(f'min_{param}')
            max_val = request.args.get(f'max_{param}')
            if min_val:
                filters[f'min_{param}'] = min_val
            if max_val:
                filters[f'max_{param}'] = max_val
        
        # Get leaderboard data
        leaderboard_data = db.get_leaderboard_data(filters)
        
        # Get available models and task groups for filters
        models = db.get_models()
        
        # Extract unique providers from config
        providers = sorted(list(set(model['provider'] for model in MODELS.values())))
        
        # Get enabled columns from session or use defaults
        from config import LEADERBOARD_COLUMNS, FILTER_SETTINGS
        enabled_columns = session.get('leaderboard_columns', 
                                    [k for k, v in LEADERBOARD_COLUMNS.items() if v['enabled']])
        
        # Get enabled filters from session or use defaults
        enabled_filters = session.get('enabled_filters',
                                    [k for k, v in FILTER_SETTINGS.items() if v['enabled']])
        
        # Build visible columns data
        visible_columns = {}
        for col_key in enabled_columns:
            if col_key in LEADERBOARD_COLUMNS:
                visible_columns[col_key] = LEADERBOARD_COLUMNS[col_key]
        
        return render_template('index.html', 
                             leaderboard=leaderboard_data,
                             models=models,
                             task_groups=TASK_GROUPS,
                             providers=providers,
                             current_filters=filters,
                             visible_columns=visible_columns,
                             enabled_columns=enabled_columns,
                             enabled_filters=enabled_filters)
    
    @app.route('/side-by-side')
    def side_by_side():
        """Side-by-side comparison page."""
        task_id = request.args.get('task_id')
        model_keys = request.args.getlist('models')
        
        # Get all available tasks and models
        tasks = db.get_tasks()
        models = db.get_models()
        
        task = None
        outputs = []
        
        if task_id:
            # Get task info
            task = next((t for t in tasks if t['task_id'] == task_id), None)
            
            if task:
                # Get outputs for comparison
                outputs = db.get_task_outputs(task_id, model_keys if model_keys else None)
        
        return render_template('side_by_side.html',
                             task=task,
                             tasks=tasks,
                             outputs=outputs,
                             models=models,
                             selected_models=model_keys)
    
    @app.route('/model/<model_key>')
    def model_detail(model_key: str):
        """Model detail page."""
        model = db.get_model_details(model_key)
        
        if not model:
            flash('Model not found')
            return redirect(url_for('index'))
        
        # Get task group performance comparison data
        task_group_data = db.get_task_group_performance(model_key=model_key, limit_groups=5)
        
        return render_template('model.html', 
                             model=model, 
                             task_group_data=task_group_data)
    
    @app.route('/import')
    def import_page():
        """Import data page."""
        return render_template('import.html')
    
    # API endpoints
    @app.route('/api/models')
    def api_models():
        """Get list of models with optional filtering."""
        filters = {}
        
        # Boolean filters
        for param in ['open_source', 'reasoning']:
            value = request.args.get(param)
            if value and value.lower() in ['true', 'false']:
                filters[param] = value.lower() == 'true'
        
        # String filters
        for param in ['tag', 'language']:
            value = request.args.get(param)
            if value:
                filters[param] = value
        
        models = db.get_models(**filters)
        
        return jsonify({
            'success': True,
            'models': models,
            'count': len(models)
        })
    
    @app.route('/api/leaderboard')
    def api_leaderboard():
        """Get leaderboard data with filtering and sorting."""
        filters = {}
        
        # Boolean filters
        for param in ['open_source', 'reasoning']:
            value = request.args.get(param)
            if value and value.lower() in ['true', 'false']:
                filters[param] = value.lower() == 'true'
        
        # String filters
        for param in ['tag', 'task_group', 'language', 'sort_by']:
            value = request.args.get(param)
            if value:
                filters[param] = value
        
        # Numeric filters
        for param in ['min_tokens']:
            value = request.args.get(param)
            if value:
                try:
                    filters[param] = int(value)
                except ValueError:
                    continue
        
        # Metric filters
        for key, value in request.args.items():
            if key.startswith('metric_') and key.endswith('_min'):
                try:
                    filters[key] = float(value)
                except ValueError:
                    continue
        
        leaderboard = db.get_leaderboard_data(filters)
        
        return jsonify({
            'success': True,
            'leaderboard': leaderboard,
            'count': len(leaderboard),
            'filters': filters
        })
    
    @app.route('/api/tasks')
    def api_tasks():
        """Get list of tasks with optional filtering."""
        task_group = request.args.get('task_group')
        tasks = db.get_tasks(task_group)
        
        return jsonify({
            'success': True,
            'tasks': tasks,
            'count': len(tasks)
        })
    
    @app.route('/api/task/<task_id>/outputs')
    def api_task_outputs(task_id: str):
        """Get outputs for a specific task, optionally filtered by models."""
        models_param = request.args.get('models')
        model_keys = models_param.split(',') if models_param else None
        
        outputs = db.get_task_outputs(task_id, model_keys)
        
        # Get task info
        tasks = db.get_tasks()
        task = next((t for t in tasks if t['task_id'] == task_id), None)
        
        return jsonify({
            'success': True,
            'task': task,
            'outputs': outputs,
            'count': len(outputs)
        })
    
    @app.route('/api/model/<model_key>')
    def api_model_detail(model_key: str):
        """Get detailed information about a specific model."""
        model = db.get_model_details(model_key)
        
        if not model:
            return jsonify({'error': 'Model not found'}), 404
        
        return jsonify({
            'success': True,
            'model': model
        })
    
    @app.route('/api/import', methods=['POST'])
    def api_import():
        """Import data from uploaded Excel/CSV file."""
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed: {ALLOWED_EXTENSIONS}'}), 400
        
        try:
            # Save uploaded file temporarily
            filename = secure_filename(file.filename)
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                file.save(tmp_file.name)
                tmp_path = tmp_file.name
            
            # Get import options
            compute_metrics = request.form.get('compute_metrics', 'true').lower() == 'true'
            dry_run = request.form.get('dry_run', 'false').lower() == 'true'
            
            # Import data
            importer = ExcelImporter(db)
            result = importer.import_data(
                tmp_path,
                compute_metrics=compute_metrics,
                dry_run=dry_run
            )
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            return jsonify(result)
            
        except Exception as e:
            # Clean up temporary file if it exists
            if 'tmp_path' in locals():
                try:
                    os.unlink(tmp_path)
                except:
                    pass
            
            return jsonify({'error': str(e)}), 500
    
    # Additional utility endpoints
    @app.route('/api/stats')
    def api_stats():
        """Get overall statistics."""
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM models")
            models_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tasks")
            tasks_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM outputs")
            outputs_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM metrics")
            metrics_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM imports")
            imports_count = cursor.fetchone()[0]
            
            # Get task groups distribution
            cursor.execute("SELECT task_group, COUNT(*) FROM tasks GROUP BY task_group")
            task_groups = dict(cursor.fetchall())
            
        return jsonify({
            'success': True,
            'stats': {
                'models': models_count,
                'tasks': tasks_count,
                'outputs': outputs_count,
                'metrics': metrics_count,
                'imports': imports_count,
                'task_groups': task_groups
            }
        })

    @app.route('/settings')
    def settings():
        """Settings page"""
        from config import LEADERBOARD_COLUMNS, FILTER_SETTINGS
        
        # Get current enabled columns from session or use defaults
        enabled_columns = session.get('leaderboard_columns', 
                                    [k for k, v in LEADERBOARD_COLUMNS.items() if v['enabled']])
        
        # Get current enabled filters from session or use defaults
        enabled_filters = session.get('enabled_filters',
                                    [k for k, v in FILTER_SETTINGS.items() if v['enabled']])
        
        # Build available columns with current enabled state
        available_columns = {}
        for col_key, col_info in LEADERBOARD_COLUMNS.items():
            available_columns[col_key] = {
                'label': col_info['label'],
                'enabled': col_key in enabled_columns,
                'order': col_info['order']
            }
        
        # Build available filters with current enabled state
        available_filters = {}
        for filter_key, filter_info in FILTER_SETTINGS.items():
            available_filters[filter_key] = {
                'label': filter_info['label'],
                'enabled': filter_key in enabled_filters,
                'order': filter_info['order']
            }
        
        return render_template('settings.html', 
                             available_columns=available_columns,
                             current_enabled_columns=enabled_columns,
                             available_filters=available_filters,
                             current_enabled_filters=enabled_filters)

    @app.route('/api/settings/columns', methods=['POST'])
    def save_column_settings():
        """Save leaderboard column settings"""
        try:
            data = request.json
            enabled_columns = data.get('enabled_columns', [])
            
            # Validate that required columns are included
            required_columns = ['rank', 'model', 'actions']
            for col in required_columns:
                if col not in enabled_columns:
                    enabled_columns.append(col)
            
            # Store in session (could be extended to database/file storage)
            session['leaderboard_columns'] = enabled_columns
            
            return jsonify({'success': True, 'enabled_columns': enabled_columns})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/settings/filters', methods=['POST'])
    def save_filter_settings():
        """Save filter visibility settings"""
        try:
            data = request.json
            enabled_filters = data.get('enabled_filters', [])
            
            # Store in session
            session['enabled_filters'] = enabled_filters
            
            return jsonify({'success': True, 'enabled_filters': enabled_filters})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/settings/filters/reset', methods=['POST'])
    def reset_filter_settings():
        """Reset filter settings to default"""
        try:
            from config import FILTER_SETTINGS
            default_filters = [k for k, v in FILTER_SETTINGS.items() if v['enabled']]
            session['enabled_filters'] = default_filters
            
            return jsonify({'success': True, 'enabled_filters': default_filters})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/settings/columns/reset', methods=['POST'])
    def reset_column_settings():
        """Reset column settings to default"""
        try:
            from config import LEADERBOARD_COLUMNS
            default_columns = [k for k, v in LEADERBOARD_COLUMNS.items() if v['enabled']]
            session['leaderboard_columns'] = default_columns
            
            return jsonify({'success': True, 'enabled_columns': default_columns})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return app


def main():
    """Run the Flask application."""
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)


if __name__ == '__main__':
    main()