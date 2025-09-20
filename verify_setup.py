"""
Quick setup verification script for LLM Leaderboard.
Run this after installation to verify everything works.
"""

import os
import sys
import json
from datetime import datetime

def test_imports():
    """Test all major imports work."""
    print("Testing imports...")
    try:
        from database import DatabaseManager
        from app import create_app
        from eval.compute_metrics import MetricsCalculator
        from scripts.import_excel import ExcelImporter
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_database():
    """Test database operations."""
    print("Testing database...")
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        
        # Test basic queries
        models = db.get_models()
        tasks = db.get_tasks()
        leaderboard = db.get_leaderboard_data()
        
        print(f"✓ Database working - {len(models)} models, {len(tasks)} tasks")
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_metrics():
    """Test metrics computation."""
    print("Testing metrics computation...")
    try:
        from eval.compute_metrics import MetricsCalculator
        calc = MetricsCalculator()
        
        metrics = calc.compute_all_metrics(
            "Hello world, this is a test.",
            "Hello universe, this is a test."
        )
        
        expected_metrics = ['bleu', 'rouge_l', 'bert_score', 'exact_match', 
                          'semantic_similarity', 'length_ratio']
        
        all_present = all(metric in metrics for metric in expected_metrics)
        print(f"✓ Metrics computation working - {len(metrics)} metrics computed")
        
        if all_present:
            print("  Available metrics:", ", ".join(metrics.keys()))
            return True
        else:
            print("✗ Some expected metrics missing")
            return False
            
    except Exception as e:
        print(f"✗ Metrics test failed: {e}")
        return False

def test_flask_app():
    """Test Flask app creation."""
    print("Testing Flask application...")
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test API endpoints
            response = client.get('/api/models')
            assert response.status_code == 200
            
            response = client.get('/api/leaderboard')
            assert response.status_code == 200
            
            response = client.get('/api/stats')
            assert response.status_code == 200
        
        print("✓ Flask app and API endpoints working")
        return True
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        return False

def test_sample_data():
    """Test sample data availability."""
    print("Testing sample data...")
    sample_file = os.path.join('data', 'sample.xlsx')
    
    if os.path.exists(sample_file):
        print("✓ Sample data file found")
        
        # Test if we can read it
        try:
            import pandas as pd
            df = pd.read_excel(sample_file)
            print(f"  - {len(df)} rows, {len(df.columns)} columns")
            print(f"  - {df['task_id'].nunique()} unique tasks")
            print(f"  - {df['model_key'].nunique()} unique models")
            return True
        except Exception as e:
            print(f"✗ Error reading sample data: {e}")
            return False
    else:
        print("✗ Sample data file not found")
        print(f"  Run: python scripts\\generate_sample_data.py")
        return False

def test_configuration():
    """Test configuration."""
    print("Testing configuration...")
    try:
        from config import MODELS, TASK_GROUPS, SUPPORTED_METRICS
        
        print(f"✓ Configuration loaded")
        print(f"  - {len(MODELS)} models configured")
        print(f"  - {len(TASK_GROUPS)} task groups")
        print(f"  - {len(SUPPORTED_METRICS)} supported metrics")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("LLM Leaderboard Setup Verification")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Test time: {datetime.now()}")
    print()
    
    tests = [
        test_imports,
        test_configuration,
        test_database,
        test_metrics,
        test_flask_app,
        test_sample_data
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your LLM Leaderboard setup is ready.")
        print()
        print("Next steps:")
        print("1. Start the application:")
        print("   $env:FLASK_APP = 'app.py'")
        print("   flask run --host=0.0.0.0")
        print()
        print("2. Import sample data:")
        print("   python scripts\\import_excel.py data\\sample.xlsx")
        print()
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        
    print("=" * 50)

if __name__ == "__main__":
    main()