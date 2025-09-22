"""
Database models and initialization for LLM Leaderboard.
Creates SQLite database with required tables and provides utility functions.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from config import DATABASE, DATA_DIR, MODELS


class DatabaseManager:
    """Manages SQLite database operations for LLM results."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.join(DATA_DIR, DATABASE)
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Ensure data directory exists."""
        os.makedirs(DATA_DIR, exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with JSON support."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        # Enable WAL mode for better concurrency
        conn.execute('PRAGMA journal_mode=WAL')
        return conn
    
    def init_database(self) -> None:
        """Initialize database with required tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create models table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS models (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_key TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    meta TEXT NOT NULL,  -- JSON data
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    prompt_text TEXT NOT NULL,
                    task_group TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create outputs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS outputs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    model_key TEXT NOT NULL,
                    output_text TEXT NOT NULL,
                    tokens INTEGER,
                    length INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks (task_id),
                    FOREIGN KEY (model_key) REFERENCES models (model_key),
                    UNIQUE(task_id, model_key)
                )
            """)
            
            # Create metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    output_id INTEGER NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (output_id) REFERENCES outputs (id),
                    UNIQUE(output_id, metric_name)
                )
            """)
            
            # Create imports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS imports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_file TEXT NOT NULL,
                    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT
                )
            """)
            
            # Create indexes for better query performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_outputs_task_model ON outputs(task_id, model_key)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_output ON metrics(output_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(metric_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_group ON tasks(task_group)")
            
            conn.commit()
            print("Database initialized successfully.")
    
    def populate_models(self) -> None:
        """Populate models table with configuration data."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for model_key, meta in MODELS.items():
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO models (model_key, name, meta)
                        VALUES (?, ?, ?)
                    """, (model_key, meta['name'], json.dumps(meta)))
                except Exception as e:
                    print(f"Error inserting model {model_key}: {e}")
            
            conn.commit()
            print(f"Populated {len(MODELS)} models.")
    
    def get_models(self, open_source: Optional[bool] = None, 
                   tag: Optional[str] = None, 
                   reasoning: Optional[bool] = None,
                   language: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get models with optional filtering."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT model_key, name, meta FROM models")
            
            models = []
            for row in cursor.fetchall():
                meta = json.loads(row['meta'])
                model = {
                    'model_key': row['model_key'],
                    'name': row['name'],
                    **meta
                }
                
                # Apply filters
                if open_source is not None and meta.get('open_source') != open_source:
                    continue
                if tag and tag not in meta.get('tags', []):
                    continue
                if reasoning is not None and meta.get('reasoning') != reasoning:
                    continue
                if language and language not in meta.get('languages', []):
                    continue
                
                models.append(model)
            
            return models
    
    def get_tasks(self, task_group: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tasks with optional filtering."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM tasks"
            params = []
            
            if task_group:
                query += " WHERE task_group = ?"
                params.append(task_group)
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_task_outputs(self, task_id: str, model_keys: List[str] = None) -> List[Dict[str, Any]]:
        """Get outputs for a specific task, optionally filtered by models."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    o.*, 
                    m.name as model_name, 
                    m.meta as model_meta,
                    GROUP_CONCAT(met.metric_name || ':' || met.metric_value) as metrics
                FROM outputs o
                JOIN models m ON o.model_key = m.model_key
                LEFT JOIN metrics met ON o.id = met.output_id
                WHERE o.task_id = ?
            """
            params = [task_id]
            
            if model_keys:
                placeholders = ','.join('?' * len(model_keys))
                query += f" AND o.model_key IN ({placeholders})"
                params.extend(model_keys)
                
            query += " GROUP BY o.id, m.name, m.meta"
            
            cursor.execute(query, params)
            results = []
            
            for row in cursor.fetchall():
                result = dict(row)
                result['model_meta'] = json.loads(row['model_meta'])
                
                # Parse metrics and add them directly to result object
                if row['metrics']:
                    for metric_pair in row['metrics'].split(','):
                        name, value = metric_pair.split(':')
                        result[name] = float(value)
                
                # Ensure all metric fields exist (set to None if missing)
                for metric in ['quality_score', 'rouge_l', 'bert_score', 'semantic_similarity', 'exact_match']:
                    if metric not in result:
                        result[metric] = None
                        
                results.append(result)
            
            return results
    
    def get_leaderboard_data(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get aggregated leaderboard data with filtering."""
        filters = filters or {}
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Base query with model metadata filtering
            # Exclude research_018 from quality score averages as many models lack research capabilities
            query = """
                SELECT 
                    m.model_key,
                    m.name,
                    m.meta,
                    COUNT(DISTINCT o.task_id) as task_count,
                    AVG(o.tokens) as avg_tokens,
                    AVG(CASE 
                        WHEN met.metric_name = 'quality_score' AND o.task_id != 'research_018' 
                        THEN met.metric_value 
                    END) as avg_quality_score,
                    AVG(CASE WHEN met.metric_name = 'rouge_l' THEN met.metric_value END) as avg_rouge_l,
                    AVG(CASE WHEN met.metric_name = 'bert_score' THEN met.metric_value END) as avg_bert_score
                FROM models m
                LEFT JOIN outputs o ON m.model_key = o.model_key
                LEFT JOIN metrics met ON o.id = met.output_id
                LEFT JOIN tasks t ON o.task_id = t.task_id
                WHERE 1=1
            """
            params = []
            
            # Apply task group filter
            if filters.get('task_group'):
                query += " AND t.task_group = ?"
                params.append(filters['task_group'])
            
            query += " GROUP BY m.model_key, m.name, m.meta"
            
            # Apply sorting
            sort_by = filters.get('sort_by', 'avg_quality_score')
            if sort_by in ['avg_quality_score', 'avg_rouge_l', 'avg_bert_score', 'avg_tokens', 'task_count']:
                query += f" ORDER BY {sort_by} DESC NULLS LAST"
            
            cursor.execute(query, params)
            results = []
            
            for row in cursor.fetchall():
                meta = json.loads(row['meta'])
                result = dict(row)
                result['meta'] = meta
                
                # Apply metadata-based filters
                if filters.get('open_source') is not None and meta.get('open_source') != filters['open_source']:
                    continue
                if filters.get('reasoning') is not None and meta.get('reasoning') != filters['reasoning']:
                    continue
                if filters.get('image_input') is not None and meta.get('image_input') != filters['image_input']:
                    continue
                if filters.get('provider') and meta.get('provider') != filters['provider']:
                    continue
                if filters.get('tag') and filters['tag'] not in meta.get('tags', []):
                    continue
                if filters.get('language') and filters['language'] not in meta.get('languages', []):
                    continue
                
                # Apply numeric range filters with type conversion
                def safe_int(value, default=0):
                    """Safely convert value to int, handling strings like '1000B'."""
                    if isinstance(value, int):
                        return value
                    if isinstance(value, str):
                        # Remove 'B' suffix if present and convert
                        cleaned = value.rstrip('B').rstrip('b')
                        try:
                            return int(cleaned)
                        except ValueError:
                            return default
                    return default
                
                def safe_context_int(value, default=0):
                    """Safely convert context window value to int, handling strings like '128K'."""
                    if isinstance(value, int):
                        return value
                    if isinstance(value, str):
                        # Remove 'K' suffix if present and convert
                        cleaned = value.rstrip('K').rstrip('k')
                        try:
                            return int(cleaned)
                        except ValueError:
                            return default
                    return default
                
                # Parameters filtering
                if filters.get('min_parameters'):
                    params_value = safe_int(meta.get('parameters', 0))
                    if params_value < filters['min_parameters']:
                        continue
                if filters.get('max_parameters'):
                    params_value = safe_int(meta.get('parameters', 0))
                    if params_value > filters['max_parameters']:
                        continue
                        
                # Context window filtering
                if filters.get('min_context'):
                    context_value = safe_context_int(meta.get('context_window', 0))
                    if context_value < filters['min_context']:
                        continue
                if filters.get('max_context'):
                    context_value = safe_context_int(meta.get('context_window', 0))
                    if context_value > filters['max_context']:
                        continue
                
                # Apply date range filters
                if filters.get('min_date') and meta.get('release_date', '') < filters['min_date']:
                    continue
                if filters.get('max_date') and meta.get('release_date', '') > filters['max_date']:
                    continue
                
                results.append(result)
            
            return results
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        """Get all available tasks."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY task_id")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_model_details(self, model_key: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific model."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get model basic info
            cursor.execute("SELECT * FROM models WHERE model_key = ?", (model_key,))
            model_row = cursor.fetchone()
            
            if not model_row:
                return None
            
            model = dict(model_row)
            model['meta'] = json.loads(model['meta'])
            
            # Get per-task metrics
            cursor.execute("""
                SELECT 
                    t.task_id,
                    t.task_name,
                    t.task_group,
                    o.tokens,
                    GROUP_CONCAT(met.metric_name || ':' || met.metric_value) as metrics
                FROM outputs o
                JOIN tasks t ON o.task_id = t.task_id
                LEFT JOIN metrics met ON o.id = met.output_id
                WHERE o.model_key = ?
                GROUP BY t.task_id, t.task_name, t.task_group, o.tokens
            """, (model_key,))
            
            tasks = []
            for row in cursor.fetchall():
                task = dict(row)
                # Parse metrics and add them directly to task object
                if row['metrics']:
                    for metric_pair in row['metrics'].split(','):
                        name, value = metric_pair.split(':')
                        task[name] = float(value)
                
                # Ensure all metric fields exist (set to None if missing)
                for metric in ['quality_score', 'rouge_l', 'bert_score', 'semantic_similarity', 'exact_match']:
                    if metric not in task:
                        task[metric] = None
                        
                tasks.append(task)
            
            model['tasks'] = tasks
            return model
    
    def insert_import_record(self, source_file: str, notes: str = None) -> int:
        """Insert import record and return its ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO imports (source_file, notes)
                VALUES (?, ?)
            """, (source_file, notes))
            conn.commit()
            return cursor.lastrowid

    def get_task_group_performance(self, model_key=None, limit_groups=5):
        """Get task group performance statistics for comparison charts."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get task group performance for all models
            cursor.execute("""
                SELECT 
                    m.model_key,
                    m.name,
                    t.task_group,
                    AVG(CASE WHEN me.metric_name = 'quality_score' AND me.metric_value IS NOT NULL 
                             THEN me.metric_value ELSE 0 END) as avg_score,
                    COUNT(DISTINCT o.id) as task_count
                FROM models m
                LEFT JOIN outputs o ON m.model_key = o.model_key
                LEFT JOIN tasks t ON o.task_id = t.task_id
                LEFT JOIN metrics me ON o.id = me.output_id AND me.metric_name = 'quality_score'
                WHERE t.task_group IS NOT NULL
                    AND t.task_id != 'research_018'  -- Exclude research task from comparison
                GROUP BY m.model_key, m.name, t.task_group
                HAVING task_count > 0
                ORDER BY t.task_group, avg_score DESC
            """)
            
            results = cursor.fetchall()
            
            # Organize results by task group
            task_groups = {}
            for model_key_db, name, task_group, avg_score, task_count in results:
                if task_group not in task_groups:
                    task_groups[task_group] = []
                task_groups[task_group].append({
                    'model_key': model_key_db,
                    'name': name,
                    'avg_score': float(avg_score) if avg_score else 0.0,
                    'task_count': task_count
                })
            
            # Limit to specified number of task groups
            from config import TASK_GROUPS
            limited_groups = TASK_GROUPS[:limit_groups]
            
            # Filter and prepare comparison data
            comparison_data = {}
            for group in limited_groups:
                if group in task_groups:
                    # Sort models by score for this group
                    sorted_models = sorted(task_groups[group], key=lambda x: x['avg_score'], reverse=True)
                    
                    if model_key:
                        # Find target model and get surrounding models for comparison
                        target_model = next((m for m in sorted_models if m['model_key'] == model_key), None)
                        if target_model:
                            target_index = sorted_models.index(target_model)
                            
                            # Get 7 other models around target model (total 8 models including target)
                            # Try to get 3-4 models before and 3-4 models after
                            before_count = min(3, target_index)
                            after_count = min(4, len(sorted_models) - target_index - 1)
                            
                            # If we don't have enough models on one side, get more from the other side
                            if before_count + after_count < 7:
                                if before_count < 3:
                                    # Get more from after if possible
                                    after_count = min(7 - before_count, len(sorted_models) - target_index - 1)
                                elif after_count < 4:
                                    # Get more from before if possible
                                    before_count = min(7 - after_count, target_index)
                            
                            start_idx = max(0, target_index - before_count)
                            end_idx = min(len(sorted_models), target_index + after_count + 1)
                            comparison_models = sorted_models[start_idx:end_idx]
                            
                            comparison_data[group] = {
                                'models': comparison_models,
                                'target_model': target_model,
                                'target_index': target_index - start_idx
                            }
                    else:
                        # Return top 5 models for each group
                        comparison_data[group] = {
                            'models': sorted_models[:5],
                            'target_model': None,
                            'target_index': -1
                        }
            
            return comparison_data


def init_database_cli():
    """CLI function to initialize database."""
    db = DatabaseManager()
    db.init_database()
    db.populate_models()
    print("Database initialization complete!")


if __name__ == "__main__":
    init_database_cli()