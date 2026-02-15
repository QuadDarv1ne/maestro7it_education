import sqlite3
import os
import shutil
import zipfile
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class BackupRestoreService:
    """Service for database backup and restore operations"""
    
    def __init__(self, db_path: str, backup_dir: str = "backups"):
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """Create a backup of the database"""
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.zip"
        
        backup_path = self.backup_dir / backup_name
        
        # Create a temporary copy of the database
        temp_db_path = self.backup_dir / "temp_backup.db"
        
        # Connect to the database and create a backup
        conn = sqlite3.connect(self.db_path)
        backup_conn = sqlite3.connect(temp_db_path)
        
        try:
            # Copy the entire database
            conn.backup(backup_conn)
            
            # Also export the schema as JSON for additional safety
            schema_data = self._export_schema(conn)
            
            # Close connections
            conn.close()
            backup_conn.close()
            
            # Create a zip archive containing the DB and schema
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_db_path, "database.db")
                
                # Save schema to JSON file inside the zip
                schema_json = json.dumps(schema_data, indent=2, default=str)
                schema_path = self.backup_dir / "schema.json"
                with open(schema_path, 'w', encoding='utf-8') as f:
                    f.write(schema_json)
                zipf.write(schema_path, "schema.json")
                
                # Add metadata
                metadata = {
                    "created_at": datetime.now().isoformat(),
                    "db_size": os.path.getsize(temp_db_path),
                    "tables": list(schema_data.keys())
                }
                metadata_json = json.dumps(metadata, indent=2)
                metadata_path = self.backup_dir / "metadata.json"
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    f.write(metadata_json)
                zipf.write(metadata_path, "metadata.json")
            
            # Clean up temporary files
            temp_db_path.unlink(missing_ok=True)
            schema_path.unlink(missing_ok=True)
            metadata_path.unlink(missing_ok=True)
            
            return str(backup_path)
        
        except Exception as e:
            # Clean up on error
            conn.close()
            backup_conn.close()
            temp_db_path.unlink(missing_ok=True)
            if backup_path.exists():
                backup_path.unlink()
            raise e
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """Restore database from a backup file"""
        backup_path = Path(backup_path)
        
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        # Extract the backup
        extract_dir = self.backup_dir / "temp_restore"
        extract_dir.mkdir(exist_ok=True)
        
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(extract_dir)
            
            # Get the database file from the extracted content
            db_file = extract_dir / "database.db"
            if not db_file.exists():
                raise FileNotFoundError("Database file not found in backup")
            
            # Backup current database before restoring
            if os.path.exists(self.db_path):
                backup_current = f"{self.db_path}.backup_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(self.db_path, backup_current)
            
            # Replace the current database with the restored one
            shutil.move(str(db_file), self.db_path)
            
            # Clean up extraction directory
            shutil.rmtree(extract_dir)
            
            return True
        
        except Exception as e:
            # Clean up extraction directory on error
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
            raise e
    
    def list_backups(self) -> List[Dict[str, any]]:
        """List all available backups"""
        backups = []
        
        for file_path in self.backup_dir.glob("*.zip"):
            stat = file_path.stat()
            backup_info = {
                "name": file_path.name,
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_mtime),
                "path": str(file_path)
            }
            backups.append(backup_info)
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        return backups
    
    def delete_backup(self, backup_name: str) -> bool:
        """Delete a specific backup file"""
        backup_path = self.backup_dir / backup_name
        
        if backup_path.exists():
            backup_path.unlink()
            return True
        return False
    
    def _export_schema(self, conn: sqlite3.Connection) -> Dict[str, List[Dict]]:
        """Export database schema information"""
        schema = {}
        
        # Get all table names
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table_row in tables:
            table_name = table_row[0]
            
            # Skip SQLite internal tables
            if table_name.startswith('sqlite_'):
                continue
            
            # Get table info
            table_info = cursor.execute(f"PRAGMA table_info('{table_name}')").fetchall()
            columns = []
            
            for col_info in table_info:
                column = {
                    "cid": col_info[0],
                    "name": col_info[1],
                    "type": col_info[2],
                    "notnull": bool(col_info[3]),
                    "default_value": col_info[4],
                    "pk": bool(col_info[5])
                }
                columns.append(column)
            
            schema[table_name] = columns
        
        return schema
    
    def validate_backup(self, backup_path: str) -> Dict[str, any]:
        """Validate a backup file"""
        backup_path = Path(backup_path)
        
        if not backup_path.exists():
            return {"valid": False, "error": "Backup file not found"}
        
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Check if required files exist in the backup
                file_list = zipf.namelist()
                
                if "database.db" not in file_list:
                    return {"valid": False, "error": "Database file missing in backup"}
                
                if "metadata.json" not in file_list:
                    return {"valid": False, "error": "Metadata file missing in backup"}
                
                # Try to read the metadata
                metadata_content = zipf.read("metadata.json").decode('utf-8')
                metadata = json.loads(metadata_content)
                
                return {
                    "valid": True,
                    "metadata": metadata,
                    "files": file_list
                }
        
        except zipfile.BadZipFile:
            return {"valid": False, "error": "Invalid zip file"}
        except json.JSONDecodeError:
            return {"valid": False, "error": "Invalid metadata in backup"}
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def get_backup_size(self, backup_path: str) -> int:
        """Get the size of a backup file"""
        return os.path.getsize(backup_path)


class DatabaseBackupManager:
    """Wrapper class for backward compatibility"""
    
    def __init__(self, db_path: str, backup_dir: str = "backups"):
        self.service = BackupRestoreService(db_path, backup_dir)
    
    def create_compressed_backup(self) -> str:
        """Create a compressed backup of the database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"chess_calendar_backup_{timestamp}.zip"
        return self.service.create_backup(backup_name)


class DataExportManager:
    """Manager for exporting data in various formats"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def export_tournaments_to_json(self, output_path: str) -> bool:
        """Export tournaments to JSON format"""
        try:
            import json
            from app import create_app, db
            from app.models.tournament import Tournament
            
            app = create_app()
            with app.app_context():
                tournaments = Tournament.query.all()
                data = [t.to_dict() for t in tournaments]
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    def export_tournaments_to_csv(self, output_path: str) -> bool:
        """Export tournaments to CSV format"""
        try:
            import csv
            from app import create_app, db
            from app.models.tournament import Tournament
            
            app = create_app()
            with app.app_context():
                tournaments = Tournament.query.all()
                
                with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['id', 'name', 'start_date', 'end_date', 'location', 
                                'category', 'status', 'description', 'prize_fund', 'organizer', 'fide_id']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for t in tournaments:
                        writer.writerow({
                            'id': t.id,
                            'name': t.name,
                            'start_date': t.start_date,
                            'end_date': t.end_date,
                            'location': t.location,
                            'category': t.category,
                            'status': t.status,
                            'description': t.description,
                            'prize_fund': t.prize_fund,
                            'organizer': t.organizer,
                            'fide_id': t.fide_id
                        })
            
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False