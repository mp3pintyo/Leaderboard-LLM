"""
Excel/CSV import script for LLM results data.
Supports configurable column mapping and validates data before import.
"""

import pandas as pd
import json
import os
import sys
import argparse
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from config import ALLOWED_EXTENSIONS, DEFAULT_COLUMN_MAPPING, MODELS
from eval.compute_metrics import MetricsCalculator


class ExcelImporter:
    """Handles import of Excel/CSV files with configurable column mapping."""
    
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()
        self.metrics_calc = MetricsCalculator()
        
    def load_column_mapping(self, mapping_file: str) -> Dict[str, str]:
        """Load column mapping from JSON file."""
        try:
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            return mapping
        except FileNotFoundError:
            print(f"Mapping file {mapping_file} not found, using default mapping.")
            return DEFAULT_COLUMN_MAPPING
        except json.JSONDecodeError as e:
            print(f"Error parsing mapping file: {e}")
            return DEFAULT_COLUMN_MAPPING
    
    def validate_file_format(self, file_path: str) -> bool:
        """Validate file extension."""
        _, ext = os.path.splitext(file_path.lower())
        return ext in ALLOWED_EXTENSIONS
    
    def load_data_file(self, file_path: str) -> pd.DataFrame:
        """Load Excel or CSV file into DataFrame."""
        _, ext = os.path.splitext(file_path.lower())
        
        try:
            if ext == '.xlsx':
                df = pd.read_excel(file_path, engine='openpyxl')
            elif ext == '.csv':
                df = pd.read_csv(file_path, encoding='utf-8')
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            
            print(f"Loaded {len(df)} rows from {file_path}")
            return df
            
        except Exception as e:
            raise Exception(f"Error loading file {file_path}: {e}")
    
    def validate_columns(self, df: pd.DataFrame, mapping: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Validate that required columns exist in the DataFrame."""
        required_cols = ['task_id', 'model_key', 'output_text']
        missing_cols = []
        
        for req_col in required_cols:
            if req_col not in mapping:
                missing_cols.append(f"Required column '{req_col}' not found in mapping")
                continue
                
            mapped_col = mapping[req_col]
            if mapped_col not in df.columns:
                missing_cols.append(f"Column '{mapped_col}' (mapped from '{req_col}') not found in data")
        
        return len(missing_cols) == 0, missing_cols
    
    def validate_data_quality(self, df: pd.DataFrame, mapping: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Validate data quality and constraints."""
        issues = []
        
        # Check for required fields (updated list)
        required_fields = ['task_id', 'task_name', 'prompt_text', 'task_group', 'model_key', 'quality_score']
        
        for req_field in required_fields:
            col = mapping.get(req_field)
            if not col:
                issues.append(f"Required field '{req_field}' not found in column mapping")
                continue
                
            if col not in df.columns:
                issues.append(f"Required column '{col}' not found in data")
                continue
                
            null_count = df[col].isnull().sum()
            if null_count > 0:
                issues.append(f"Required column '{col}' has {null_count} null values")
        
        # Validate model keys
        model_col = mapping.get('model_key')
        if model_col and model_col in df.columns:
            invalid_models = df[~df[model_col].isin(MODELS.keys())][model_col].unique()
            if len(invalid_models) > 0:
                issues.append(f"Invalid model keys found: {list(invalid_models)}")
        
        # Validate quality_score range (0-10)
        quality_col = mapping.get('quality_score')
        if quality_col and quality_col in df.columns:
            try:
                quality_scores = pd.to_numeric(df[quality_col], errors='coerce')
                invalid_scores = quality_scores[(quality_scores < 0) | (quality_scores > 10)]
                if len(invalid_scores) > 0:
                    issues.append(f"Quality scores must be between 0-10. Found {len(invalid_scores)} invalid values")
            except:
                issues.append(f"Column '{quality_col}' contains non-numeric values")
        
        # Validate optional numeric fields
        for num_field in ['tokens', 'length']:
            col = mapping.get(num_field)
            if col and col in df.columns:
                try:
                    pd.to_numeric(df[col], errors='coerce')
                except:
                    issues.append(f"Column '{col}' contains non-numeric values")
        
        return len(issues) == 0, issues
    
    def prepare_data(self, df: pd.DataFrame, mapping: Dict[str, str]) -> Tuple[List[Dict], List[Dict]]:
        """Prepare tasks and outputs data for database insertion."""
        tasks_data = []
        outputs_data = []
        
        # Process each row
        for _, row in df.iterrows():
            # Prepare task data (all required fields)
            task_data = {
                'task_id': str(row[mapping['task_id']]),
                'task_name': str(row[mapping['task_name']]),
                'prompt_text': str(row[mapping['prompt_text']]),
                'task_group': str(row[mapping['task_group']])
            }
            
            # Avoid duplicates in tasks_data
            if not any(t['task_id'] == task_data['task_id'] for t in tasks_data):
                tasks_data.append(task_data)
            
            # Prepare output data
            output_data = {
                'task_id': task_data['task_id'],
                'model_key': str(row[mapping['model_key']]),
                'output_text': str(row.get(mapping.get('output_text', ''), '')),  # Optional now
                'tokens': self._safe_int_convert(row.get(mapping.get('tokens', ''), None)),
                'quality_score': self._safe_float_convert(row[mapping['quality_score']])  # Required
            }
            outputs_data.append(output_data)
        
        return tasks_data, outputs_data
    
    def _safe_int_convert(self, value) -> Optional[int]:
        """Safely convert value to integer."""
        if pd.isna(value) or value == '':
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None
    
    def _safe_float_convert(self, value) -> Optional[float]:
        """Safely convert value to float."""
        if pd.isna(value) or value == '':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def import_data(self, file_path: str, mapping_file: str = None, 
                   compute_metrics: bool = True, dry_run: bool = False) -> Dict[str, Any]:
        """Import data from Excel/CSV file."""
        
        # Load mapping
        mapping_path = mapping_file or os.path.join('data', 'mapping.json')
        mapping = self.load_column_mapping(mapping_path)
        
        # Validate file
        if not self.validate_file_format(file_path):
            raise ValueError(f"Unsupported file format. Allowed: {ALLOWED_EXTENSIONS}")
        
        # Load data
        df = self.load_data_file(file_path)
        
        # Validate columns
        columns_valid, column_issues = self.validate_columns(df, mapping)
        if not columns_valid:
            raise ValueError(f"Column validation failed: {'; '.join(column_issues)}")
        
        # Validate data quality
        data_valid, data_issues = self.validate_data_quality(df, mapping)
        if not data_valid:
            print(f"Data quality warnings: {'; '.join(data_issues)}")
        
        # Prepare data
        tasks_data, outputs_data = self.prepare_data(df, mapping)
        
        if dry_run:
            return {
                'success': True,
                'dry_run': True,
                'tasks_count': len(tasks_data),
                'outputs_count': len(outputs_data),
                'tasks_preview': tasks_data[:3],
                'outputs_preview': outputs_data[:3],
                'warnings': data_issues
            }
        
        # Import to database
        return self._execute_import(file_path, tasks_data, outputs_data, compute_metrics)
    
    def _execute_import(self, file_path: str, tasks_data: List[Dict], 
                       outputs_data: List[Dict], compute_metrics: bool) -> Dict[str, Any]:
        """Execute the actual database import with better transaction handling."""
        
        print(f"Starting import: {len(tasks_data)} tasks, {len(outputs_data)} outputs")
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Insert tasks in batch
            tasks_inserted = 0
            print("Importing tasks...")
            for task in tasks_data:
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO tasks (task_id, task_name, prompt_text, task_group)
                        VALUES (?, ?, ?, ?)
                    """, (task['task_id'], task['task_name'], task['prompt_text'], task['task_group']))
                    tasks_inserted += 1
                except Exception as e:
                    print(f"Error inserting task {task['task_id']}: {e}")
            
            # Commit tasks first
            conn.commit()
            print(f"Tasks committed: {tasks_inserted}")
            
            # Insert outputs in batch
            outputs_inserted = 0
            output_ids = []
            print("Importing outputs...")
            
            for i, output in enumerate(outputs_data):
                try:
                    # First, get existing output ID if it exists to clean up old metrics
                    cursor.execute("""
                        SELECT id FROM outputs WHERE task_id = ? AND model_key = ?
                    """, (output['task_id'], output['model_key']))
                    existing_output = cursor.fetchone()
                    
                    if existing_output:
                        # Delete old metrics for this output to ensure fresh data
                        cursor.execute("""
                            DELETE FROM metrics WHERE output_id = ?
                        """, (existing_output[0],))
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO outputs (task_id, model_key, output_text, tokens)
                        VALUES (?, ?, ?, ?)
                    """, (output['task_id'], output['model_key'], output['output_text'], 
                         output['tokens']))
                    
                    # Get the output ID for metrics computation
                    cursor.execute("""
                        SELECT id FROM outputs WHERE task_id = ? AND model_key = ?
                    """, (output['task_id'], output['model_key']))
                    
                    output_id = cursor.fetchone()[0]
                    output_ids.append((output_id, output))
                    outputs_inserted += 1
                    
                    if (i + 1) % 5 == 0:  # Progress feedback every 5 outputs
                        print(f"  Processed {i + 1}/{len(outputs_data)} outputs")
                    
                except Exception as e:
                    print(f"Error inserting output for task {output['task_id']}, model {output['model_key']}: {e}")
            
            # Commit outputs
            conn.commit()
            print(f"Outputs committed: {outputs_inserted}")
            
            # Compute and insert metrics with batching
            metrics_inserted = 0
            if compute_metrics:
                print("Computing metrics...")
                batch_size = 5  # Process in smaller batches
                
                for i, (output_id, output_data) in enumerate(output_ids):
                    try:
                        # Get task prompt for metrics computation
                        cursor.execute("SELECT prompt_text FROM tasks WHERE task_id = ?", (output_data['task_id'],))
                        prompt_row = cursor.fetchone()
                        reference_text = prompt_row[0] if prompt_row else ""
                        
                        # Use new method that handles quality score
                        metrics = self.metrics_calc.compute_all_metrics_with_quality(
                            reference_text, 
                            output_data['output_text'],
                            output_data.get('quality_score')
                        )
                        
                        # Batch insert metrics (skip None values)
                        for metric_name, metric_value in metrics.items():
                            if metric_value is not None:
                                cursor.execute("""
                                    INSERT OR REPLACE INTO metrics (output_id, metric_name, metric_value)
                                    VALUES (?, ?, ?)
                                """, (output_id, metric_name, metric_value))
                                metrics_inserted += 1
                        
                        # Commit every batch_size outputs to prevent long locks
                        if (i + 1) % batch_size == 0:
                            conn.commit()
                            print(f"  Metrics computed for {i + 1}/{len(output_ids)} outputs")
                            
                    except Exception as e:
                        print(f"Error computing metrics for output {output_id}: {e}")
                
                # Final commit for any remaining metrics
                conn.commit()
                print(f"Metrics computation completed: {metrics_inserted} metrics")
            
            # Record import
            import_id = self.db.insert_import_record(
                file_path, 
                f"Imported {tasks_inserted} tasks, {outputs_inserted} outputs, {metrics_inserted} metrics"
            )
            
            conn.commit()
        
        return {
            'success': True,
            'import_id': import_id,
            'tasks_inserted': tasks_inserted,
            'outputs_inserted': outputs_inserted,
            'metrics_inserted': metrics_inserted,
            'file_path': file_path
        }


def main():
    """CLI interface for the import script."""
    parser = argparse.ArgumentParser(description='Import LLM results from Excel/CSV files')
    parser.add_argument('file_path', help='Path to Excel/CSV file to import')
    parser.add_argument('--mapping', help='Path to column mapping JSON file')
    parser.add_argument('--no-metrics', action='store_true', help='Skip metrics computation')
    parser.add_argument('--dry-run', action='store_true', help='Validate without importing')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize importer
    importer = ExcelImporter()
    
    try:
        # Execute import
        result = importer.import_data(
            args.file_path,
            args.mapping,
            compute_metrics=not args.no_metrics,
            dry_run=args.dry_run
        )
        
        # Print results
        if args.dry_run:
            print("\n=== DRY RUN RESULTS ===")
            print(f"Tasks to be imported: {result['tasks_count']}")
            print(f"Outputs to be imported: {result['outputs_count']}")
            if result.get('warnings'):
                print(f"Warnings: {len(result['warnings'])}")
                for warning in result['warnings']:
                    print(f"  - {warning}")
        else:
            print("\n=== IMPORT COMPLETED ===")
            print(f"Import ID: {result['import_id']}")
            print(f"Tasks inserted: {result['tasks_inserted']}")
            print(f"Outputs inserted: {result['outputs_inserted']}")
            print(f"Metrics computed: {result['metrics_inserted']}")
        
    except Exception as e:
        print(f"Import failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()