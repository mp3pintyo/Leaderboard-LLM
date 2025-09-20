"""
Selective task deletion utility.
"""

import sqlite3
from database import DatabaseManager

def list_tasks():
    """List all current tasks."""
    db = DatabaseManager()
    tasks = db.get_tasks()
    
    if not tasks:
        print("Nincsenek task-ok az adatbázisban.")
        return
    
    print("Jelenlegi task-ok:")
    print("-" * 60)
    for task in tasks:
        print(f"ID: {task['task_id']}")
        print(f"  Név: {task['task_name']}")
        print(f"  Csoport: {task['task_group'] or 'N/A'}")
        
        # Outputs száma
        outputs = db.get_task_outputs(task['task_id'])
        print(f"  Outputs: {len(outputs)}")
        print()

def delete_task(task_id: str):
    """Delete specific task and all related data."""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Ellenőrizzük, létezik-e
        cursor.execute("SELECT task_name FROM tasks WHERE task_id = ?", (task_id,))
        task = cursor.fetchone()
        
        if not task:
            print(f"❌ Task '{task_id}' nem található!")
            return
        
        print(f"Task törlése: {task['task_name']} ({task_id})")
        
        # Kapcsolódó adatok száma
        cursor.execute("SELECT COUNT(*) FROM outputs WHERE task_id = ?", (task_id,))
        outputs_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM metrics m 
            JOIN outputs o ON m.output_id = o.id 
            WHERE o.task_id = ?
        """, (task_id,))
        metrics_count = cursor.fetchone()[0]
        
        print(f"  Törölendő outputs: {outputs_count}")
        print(f"  Törölendő metrics: {metrics_count}")
        
        response = input("Biztosan törlöd? (igen/nem): ")
        
        if response.lower() in ['igen', 'yes', 'y']:
            # Törlés
            cursor.execute("""
                DELETE FROM metrics WHERE output_id IN (
                    SELECT id FROM outputs WHERE task_id = ?
                )
            """, (task_id,))
            
            cursor.execute("DELETE FROM outputs WHERE task_id = ?", (task_id,))
            cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            
            conn.commit()
            print(f"✅ Task '{task_id}' törölve!")
        else:
            print("❌ Törlés megszakítva")

def delete_task_group(group_name: str):
    """Delete all tasks in a specific group."""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Group tasks listája
        cursor.execute("SELECT task_id, task_name FROM tasks WHERE task_group = ?", (group_name,))
        tasks = cursor.fetchall()
        
        if not tasks:
            print(f"❌ Nincs task a '{group_name}' csoportban!")
            return
        
        print(f"Csoport törlése: '{group_name}'")
        print(f"Érintett task-ok:")
        for task in tasks:
            print(f"  - {task['task_id']}: {task['task_name']}")
        
        response = input(f"Biztosan törlöd az összes '{group_name}' task-ot? (igen/nem): ")
        
        if response.lower() in ['igen', 'yes', 'y']:
            for task in tasks:
                # Minden task törlése egyesével
                cursor.execute("""
                    DELETE FROM metrics WHERE output_id IN (
                        SELECT id FROM outputs WHERE task_id = ?
                    )
                """, (task['task_id'],))
                
                cursor.execute("DELETE FROM outputs WHERE task_id = ?", (task['task_id'],))
                cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task['task_id'],))
            
            conn.commit()
            print(f"✅ '{group_name}' csoport törölve!")
        else:
            print("❌ Törlés megszakítva")

def main():
    """Interactive task management."""
    while True:
        print("\n" + "="*50)
        print("TASK KEZELŐ MENÜ")
        print("="*50)
        print("1. Task-ok listázása")
        print("2. Egy task törlése")
        print("3. Task csoport törlése")
        print("4. Kilépés")
        
        choice = input("\nVálasztás (1-4): ")
        
        if choice == '1':
            list_tasks()
            
        elif choice == '2':
            task_id = input("Task ID: ")
            delete_task(task_id)
            
        elif choice == '3':
            group_name = input("Task group név: ")
            delete_task_group(group_name)
            
        elif choice == '4':
            break
            
        else:
            print("❌ Érvénytelen választás!")

if __name__ == "__main__":
    main()