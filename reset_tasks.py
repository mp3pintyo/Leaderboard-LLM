"""
Reset only tasks table while keeping models intact.
"""

import sqlite3
import os
from database import DatabaseManager

def reset_tasks_only():
    """Reset tasks table and related data while keeping models."""
    
    db = DatabaseManager()
    
    print("Tasks reset előtt:")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Jelenlegi állapot
        cursor.execute("SELECT COUNT(*) FROM tasks")
        tasks_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM outputs") 
        outputs_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM metrics")
        metrics_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM models")
        models_count = cursor.fetchone()[0]
        
        print(f"  Tasks: {tasks_count}")
        print(f"  Outputs: {outputs_count}")
        print(f"  Metrics: {metrics_count}")
        print(f"  Models: {models_count}")
    
    # Biztonsági kérdés
    response = input("\nBiztosan törölni szeretnéd az összes task-ot és kapcsolódó adatokat? (igen/nem): ")
    
    if response.lower() in ['igen', 'yes', 'y']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            print("\nTörlés folyamatban...")
            
            # Törlés sorrendje (foreign key constraints miatt)
            cursor.execute("DELETE FROM metrics")
            print("  ✓ Metrics törölve")
            
            cursor.execute("DELETE FROM outputs") 
            print("  ✓ Outputs törölve")
            
            cursor.execute("DELETE FROM tasks")
            print("  ✓ Tasks törölve")
            
            cursor.execute("DELETE FROM imports")
            print("  ✓ Import history törölve")
            
            conn.commit()
            
        print("\n✅ Tasks reset kész!")
        print("💡 Models tábla érintetlen maradt")
        print("💡 Új adatok importálásához: python scripts\\import_excel.py data\\sample.xlsx")
        
    else:
        print("❌ Reset megszakítva")

if __name__ == "__main__":
    reset_tasks_only()