#!/usr/bin/env python3
"""
Batch import script for multiple Excel files.
Imports all Excel files from the data directory in sequence.
"""

import os
import sys
import glob
import argparse
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from import_excel import ExcelImporter
from database import DatabaseManager


def find_excel_files(directory: str, pattern: str = "sample_import_template*.xlsx") -> List[str]:
    """Find all Excel files matching the pattern in the directory."""
    search_pattern = os.path.join(directory, pattern)
    files = glob.glob(search_pattern)
    
    # Exclude the empty template file
    template_file = os.path.join(directory, "sample_import_template.xlsx")
    if template_file in files:
        files.remove(template_file)
    
    files.sort()  # Sort for consistent order
    return files


def batch_import(data_dir: str = "data", pattern: str = "sample_import_template*.xlsx", 
                compute_metrics: bool = True, verbose: bool = False) -> None:
    """Import all Excel files from the data directory."""
    
    # Find Excel files
    excel_files = find_excel_files(data_dir, pattern)
    
    if not excel_files:
        print(f"No Excel files found matching pattern '{pattern}' in '{data_dir}'")
        return
    
    print(f"Found {len(excel_files)} Excel files to import:")
    for i, file in enumerate(excel_files, 1):
        print(f"  {i}. {os.path.basename(file)}")
    
    # Initialize importer
    importer = ExcelImporter()
    
    # Import statistics
    total_imports = 0
    successful_imports = 0
    failed_imports = 0
    
    print(f"\nStarting batch import...")
    print("=" * 60)
    
    for i, file_path in enumerate(excel_files, 1):
        filename = os.path.basename(file_path)
        print(f"\n[{i}/{len(excel_files)}] Importing: {filename}")
        
        try:
            result = importer.import_data(
                file_path,
                compute_metrics=compute_metrics,
                dry_run=False
            )
            
            if result.get('success'):
                successful_imports += 1
                if verbose:
                    print(f"  ✓ Success: {result['tasks_inserted']} tasks, "
                          f"{result['outputs_inserted']} outputs, "
                          f"{result['metrics_inserted']} metrics")
                else:
                    print(f"  ✓ Success: {result['outputs_inserted']} outputs imported")
            else:
                failed_imports += 1
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            failed_imports += 1
            print(f"  ✗ Failed: {e}")
        
        total_imports += 1
    
    print("\n" + "=" * 60)
    print(f"Batch import completed!")
    print(f"Total files processed: {total_imports}")
    print(f"Successful imports: {successful_imports}")
    print(f"Failed imports: {failed_imports}")
    
    if failed_imports > 0:
        print(f"\n⚠️  {failed_imports} imports failed. Check the error messages above.")
    else:
        print(f"\n🎉 All imports completed successfully!")


def main():
    """CLI interface for batch import."""
    parser = argparse.ArgumentParser(description='Batch import Excel files from data directory')
    parser.add_argument('--data-dir', default='data', help='Directory containing Excel files (default: data)')
    parser.add_argument('--pattern', default='sample_import_template*.xlsx', 
                       help='File pattern to match (default: sample_import_template*.xlsx)')
    parser.add_argument('--no-metrics', action='store_true', help='Skip metrics computation')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        batch_import(
            data_dir=args.data_dir,
            pattern=args.pattern,
            compute_metrics=not args.no_metrics,
            verbose=args.verbose
        )
    except KeyboardInterrupt:
        print("\n\nBatch import interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nBatch import failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()