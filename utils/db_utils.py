from sqlite3 import connect, Cursor
from pathlib import Path
from typing import Optional, Union


class DbInit:
    def __init__(self, db_dir: Union[str, Path]) -> None:
        self.db_dir = db_dir
        self.db_dir.mkdir(exist_ok=True)

        self.open_index_path: Path = self.db_dir / "open_index.db"
        self.encrypted_index_path: Path = self.db_dir / "encrypted_index.db"
        self.used_index_path: Path = self.db_dir / "used_index.db"

        return None


    def initalize_all(self) -> None:
        if self.open_index_path.exists():
            print(f"Open index already exists: {self.open_index_path}")
        else:
            self._create_open_index()
        
        if self.encrypted_index_path.exists():
            print(f"Encrypted index already exists: {self.encrypted_index_path}")
        else:
            self._create_encrypted_index()
        
        if self.used_index_path.exists():
            print(f"Used index already exists: {self.used_index_path}")
        else:
            self._create_used_index()

        return None

    def _create_open_index(self) -> None:
        if self.open_index_path.exists():
            print(f"Open index already exists: {self.open_index_path}")
            return None
        
        with connect(self.open_index_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    account_name TEXT NOT NULL,
                    key_count INTEGER NOT NULL DEFAULT 0,
                    UNIQUE(platform, account_name))
            """)
            conn.commit()
            print(f"Open index created: {self.open_index_path}")

        return None

    def _create_encrypted_index(self) -> None:
        if self.encrypted_index_path.exists():
            print(f"Encrypted index already exists: {self.encrypted_index_path}")
            return None   
        
        with connect(self.encrypted_index_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE backup_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    encrypted_key TEXT NOT NULL,
                    FOREIGN KEY (account_id) REFERENCES accounts(id))
            """)
            conn.commit()
            print(f"Encrypted index created: {self.encrypted_index_path}")

        return None

    def _create_used_index(self) -> None:
        if self.used_index_path.exists():
            print(f"Used index already exists: {self.used_index_path}")
            return None
        
        with connect(self.used_index_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE used_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    account_name TEXT NOT NULL,
                    used_key TEXT NOT NULL,
                    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)
            conn.commit()
            print(f"Used index created: {self.used_index_path}")

        return None
    

class DBUtils:
    def __init__(self, db_path: Union[str, Path]) -> None:
        self.db_path = db_path

    def add_account(self, platform: Optional[str], account_name: Optional[str]) -> bool:
        try:
            with connect(self.db_path) as conn:
                cursor: Cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO accounts 
                    (platform, account_name) 
                    VALUES (?, ?)
                """, (platform, account_name))
                conn.commit()
            return True
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False
            raise e

    def add_backup_key(self, account_id: str, encrypted_key: str) -> None:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO backup_keys 
                (account_id, encrypted_key) 
                VALUES (?, ?)
            """, (account_id, encrypted_key))
            conn.commit()

    def get_account_id(self, platform: str, account_name: str) -> Optional[str]:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT id 
                FROM accounts 
                WHERE platform = ? AND account_name = ?
            """, (platform, account_name))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_backup_key(self, account_id: str) -> Optional[str]:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT encrypted_key, id 
                FROM backup_keys 
                WHERE account_id = ? 
                ORDER BY id ASC 
                LIMIT 1
            """, (account_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        
    def get_used_key(self, platform: str, account_name: str) -> Optional[str]:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT used_key 
                FROM used_keys 
                WHERE platform = ? AND account_name = ? 
                ORDER BY id ASC LIMIT 1
            """, (platform, account_name))
            result = cursor.fetchone()
            return result[0] if result else None
        
    def archive_used_key(self, platform: str, account_name: str, used_key: str) -> None:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO used_keys 
                (platform, account_name, used_key) 
                VALUES (?, ?, ?)
            """, (platform, account_name, used_key))
            conn.commit()

        return None

    def get_all_used_keys(self) -> list[tuple[str, str, str]]:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT platform,
                account_name, 
                used_key FROM used_keys
            """)
            return cursor.fetchall()
        
    def get_all_accounts(self) -> list[tuple[str, str, str]]:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT platform,
                account_name,
                id FROM accounts
            """)
            return cursor.fetchall()
        
    def get_all_backup_keys(self) -> list[tuple[str, str]]:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT account_id, encrypted_key 
                FROM backup_keys
            """)
            return cursor.fetchall()
        
    def delete_account(self, account_id: str) -> None:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM accounts 
                WHERE id = ?
            """, (account_id,))
            conn.commit()

        return None

    def delete_backup_key(self, account_id: str, backup_key_id: str) -> None:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM backup_keys 
                WHERE account_id = ? AND id = ?
            """, (account_id, backup_key_id))
            conn.commit()

        return None
    
    def delete_used_key(self, platform: str, account_name: str) -> None:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM used_keys 
                WHERE platform = ? AND account_name = ?
            """, (platform, account_name))
            conn.commit()

        return None
    
    def get_key_count(self, account_id: str) -> int:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT key_count 
                FROM accounts 
                WHERE id = ?
            """, (account_id,))
            result = cursor.fetchone()
            return result[0] if result else 0

    def increment_key_count(self, account_id: str) -> None:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts 
                SET key_count = key_count + 1 
                WHERE id = ?
            """, (account_id,))
            conn.commit()

        return None

    def decrement_key_count(self, account_id: str) -> None:
        with connect(self.db_path) as conn:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts 
                SET key_count = key_count - 1 
                WHERE id = ?
            """, (account_id,))
            conn.commit()

        return None
    

        


