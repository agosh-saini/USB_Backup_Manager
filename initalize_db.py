from sqlite3 import connect, Cursor
from pathlib import Path
from typing import Union, Optional

class DbInit:
    def __init__(self, db_dir: Union[str, Path]) -> None:
        self.db_dir = db_dir
        self.db_dir.mkdir(exist_ok=True)

        self.open_index_path: Path = self.db_dir / "open_index.db"
        self.encrypted_index_path: Path = self.db_dir / "encrypted_index.db"
        self.used_index_path: Path = self.db_dir / "used_index.db"

        return None


    def initalize_all(self) -> None:
        self._create_open_index()
        self._create_encrypted_index()
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
                                id TEXT PRIMARY KEY,
                                platform TEXT NOT NULL,
                                account_name TEXT NOT NULL,
                                key_count INTEGER NOT NULL DEFAULT 0)
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
                                id TEXT PRIMARY KEY,
                                account_id TEXT NOT NULL,
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
                                id TEXT PRIMARY KEY,
                                platform TEXT NOT NULL,
                                account_name TEXT NOT NULL,
                                used_key TEXT NOT NULL,
                                used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                            """)
            conn.commit()
            print(f"Used index created: {self.used_index_path}")

        return None
    
if __name__ == "__main__":
    initializer: DbInit = DbInit(Path("db"))
    initializer.initalize_all()
