import utils.db_utils as db_utils
from pathlib import Path

# Initialize the database directory and create all tables
db_dir = Path("db/test.db")
db_init = db_utils.DbInit(db_dir)
db_init.initalize_all()

# Create separate DBUtils instances for each database
open_db = db_utils.DBUtils(db_dir / "open_index.db")
encrypted_db = db_utils.DBUtils(db_dir / "encrypted_index.db")
used_db = db_utils.DBUtils(db_dir / "used_index.db")

# Test account operations
open_db.add_account("1", "test", "test")
open_db.add_account("2", "test", "test")

encrypted_db.add_backup_key("1", "test")
encrypted_db.add_backup_key("2", "test")

used_db.archive_used_key("test", "test", "test")    

print("Used keys:", used_db.get_all_used_keys())

used_db.delete_used_key("test", "test")

print("Used keys after delete:", used_db.get_all_used_keys())

open_db.increment_key_count("1")

print("Key count after increment:", open_db.get_key_count("1"))

open_db.decrement_key_count("1")

print("Key count after decrement:", open_db.get_key_count("1"))    

open_db.delete_account("1")

print("All accounts:", open_db.get_all_accounts())    

encrypted_db.delete_backup_key("1")

print("All backup keys:", encrypted_db.get_all_backup_keys())



























