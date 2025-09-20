"""
Database backup utility before reset operations.
"""

import shutil
import os
from datetime import datetime
from database import DatabaseManager

def create_backup():
    """Create a backup of the current database."""
    
    db_path = os.path.join('data', 'results.db')
    
    if not os.path.exists(db_path):
        print("❌ Adatbázis fájl nem található!")
        return None
    
    # Backup fájlnév timestamp-pel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join('data', f'results_backup_{timestamp}.db')
    
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup készítve: {backup_path}")
        
        # Stat info
        size_mb = os.path.getsize(backup_path) / 1024 / 1024
        print(f"   Méret: {size_mb:.2f} MB")
        
        return backup_path
        
    except Exception as e:
        print(f"❌ Backup hiba: {e}")
        return None

def restore_backup(backup_path: str):
    """Restore database from backup."""
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup fájl nem található: {backup_path}")
        return False
    
    db_path = os.path.join('data', 'results.db')
    
    response = input(f"Visszaállítod a backup-ot? Ez felülírja a jelenlegi adatbázist! (igen/nem): ")
    
    if response.lower() in ['igen', 'yes', 'y']:
        try:
            shutil.copy2(backup_path, db_path)
            print(f"✅ Adatbázis visszaállítva a backup-ból!")
            return True
        except Exception as e:
            print(f"❌ Visszaállítási hiba: {e}")
            return False
    else:
        print("❌ Visszaállítás megszakítva")
        return False

def list_backups():
    """List available backup files."""
    
    data_dir = 'data'
    backups = [f for f in os.listdir(data_dir) if f.startswith('results_backup_') and f.endswith('.db')]
    
    if not backups:
        print("Nincsenek backup fájlok.")
        return []
    
    print("Elérhető backup fájlok:")
    print("-" * 40)
    
    for backup in sorted(backups, reverse=True):
        backup_path = os.path.join(data_dir, backup)
        size_mb = os.path.getsize(backup_path) / 1024 / 1024
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_path))
        
        print(f"{backup}")
        print(f"  Létrehozva: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Méret: {size_mb:.2f} MB")
        print()
    
    return backups

def safe_reset_workflow():
    """Safe workflow for resetting tasks with backup."""
    
    print("🔒 BIZTONSÁGOS RESET FOLYAMAT")
    print("=" * 40)
    
    # 1. Backup készítése
    print("1. Backup készítése...")
    backup_path = create_backup()
    
    if not backup_path:
        print("❌ Backup sikertelen, reset megszakítva!")
        return
    
    # 2. Reset végrehajtása
    print("\n2. Reset opciók:")
    print("a) Teljes adatbázis reset")
    print("b) Csak tasks reset") 
    print("c) Szelektív task törlés")
    print("d) Mégse")
    
    choice = input("Választás (a-d): ").lower()
    
    if choice == 'a':
        response = input("Teljes reset - törlöd az EGÉSZ adatbázist? (igen/nem): ")
        if response.lower() in ['igen', 'yes', 'y']:
            os.remove('data/results.db')
            os.system('python database.py')
            print("✅ Teljes reset kész!")
            
    elif choice == 'b':
        print("Tasks reset futtatása...")
        os.system('python reset_tasks.py')
        
    elif choice == 'c':
        print("Szelektív törlés...")
        os.system('python manage_tasks.py')
        
    elif choice == 'd':
        print("❌ Reset megszakítva")
        
    else:
        print("❌ Érvénytelen választás!")
    
    print(f"\n💡 Ha baj van, visszaállíthatod: python restore_backup.py {backup_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'backup':
            create_backup()
        elif sys.argv[1] == 'list':
            list_backups()
        elif sys.argv[1] == 'restore':
            if len(sys.argv) > 2:
                restore_backup(sys.argv[2])
            else:
                backups = list_backups()
                if backups:
                    backup_name = input("Melyik backup-ot állítsam vissza? ")
                    restore_backup(os.path.join('data', backup_name))
    else:
        safe_reset_workflow()