from getpass import getpass
from click import prompt, secho

from encryption.master_key_manager import MasterKeyManager
from encryption.crypto_handler import CryptoHandler

from utils.db_utils import DBUtils

from pathlib import Path

class InputHandler:
    def __init__(self, key_manager: MasterKeyManager, crypto_handler: CryptoHandler, 
                 open_db: DBUtils, encrypted_db: DBUtils, used_db: DBUtils) -> None:
        self.master_key_manager = key_manager
        self.crypto_handler = crypto_handler
        self.open_db = open_db
        self.encrypted_db = encrypted_db
        self.used_db = used_db
        self.path = Path()
    

    def help(self) -> None:
        secho("\nBackup Key Manager - Commands", fg="green", bold=True, underline=True)
        secho("1. Add Account: add_account", fg="blue")
        secho("2. Add Backup Key: add_backup_key", fg="blue")
        secho("3. View Backup Key: view_backup_key", fg="blue")
        secho("4. View Used Key: view_used_key", fg="blue")
        secho("5. Delete Used Key: delete_used_key", fg="blue")
        secho("6. All Accounts: all_accounts", fg="blue")
        secho("7. All Backup Keys: all_backup_keys", fg="blue")
        secho("8. All Used Keys: all_used_keys", fg="blue")
        secho("9. Update Password: update_password", fg="blue")
        secho("10. Exit: exit", fg="blue")

    def add_account(self) -> None:
        platform = prompt("platform: ", fg="yellow")
        account = prompt("account: ", fg="yellow")

        if not self.open_db.add_account(platform, account):
            print("Account already exists for this platform")
            return

    def add_backup_key(self) -> None:
        platform = prompt("platform: ", fg="yellow")
        account = prompt("account: ", fg="yellow")
        key = prompt("key: ", fg="yellow")

        # Get account_id first
        account_id = self.open_db.get_account_id(platform, account)
        if account_id is None:
            # If account doesn't exist, create it
            if not self.open_db.add_account(platform, account):
                secho("Account already exists for this platform", fg="red")
                return
            account_id = self.open_db.get_account_id(platform, account)

        # Convert key to bytes before encryption
        key_bytes = key.encode()
        encrypted_key = self.crypto_handler.encrypt(key_bytes)

        self.encrypted_db.add_backup_key(account_id, encrypted_key)
        self.open_db.increment_key_count(account_id)
    
    def view_backup_key(self) -> None:
        platform = prompt("platform: ", fg="yellow")
        account = prompt("account: ", fg="yellow")
        password = prompt("password: ", fg="yellow").encode()

        # Create a temporary key manager with the provided password to verify it
        temp_key_manager = MasterKeyManager(password)
        if temp_key_manager.load_master_key() is None:
            secho("Incorrect password", fg="red")
            return

        # Get account_id first
        account_id = self.open_db.get_account_id(platform, account)
        if account_id is None:
            secho("Account not found", fg="red")
            return

        # Get the backup key with the lowest ID
        key = self.encrypted_db.get_backup_key(account_id)
        if key is None:
            secho("No backup key found", fg="red")
            return

        decrypted_key = self.crypto_handler.decrypt(key)
        if decrypted_key is None:
            secho("Failed to decrypt key", fg="red")
            return

        # Delete the backup key that was viewed
        self.encrypted_db.delete_backup_key(account_id)
        self.open_db.decrement_key_count(account_id)
        self.used_db.archive_used_key(platform, account, decrypted_key.decode())

        print(f"Key: {decrypted_key.decode()}")

    def view_used_key(self) -> None:
        platform = prompt("platform: ", fg="yellow")
        account = prompt("account: ", fg="yellow")

        key = self.used_db.get_used_key(platform, account)

        print(f"Key: {key}")

    def delete_used_key(self) -> None:
        platform = prompt("platform: ", fg="yellow")
        account = prompt("account: ", fg="yellow")
        password = prompt("password: ", fg="yellow")

        if self.master_key_manager.load_master_key(password) is None:
            secho("Incorrect password", fg="red")
            return

        self.used_db.delete_used_key(platform, account)

    def all_accounts(self) -> None:
        accounts = self.open_db.get_all_accounts()

        for account in accounts:
            secho(f"Platform: {account[0]}, Account: {account[1]}, ID: {account[2]}", fg="green")

    def all_backup_keys(self) -> None:
        backup_keys = self.encrypted_db.get_all_backup_keys()
        accounts = {acc[2]: (acc[0], acc[1]) for acc in self.open_db.get_all_accounts()}

        for backup_key in backup_keys:
            account_id = backup_key[0]
            if account_id in accounts:
                platform, account = accounts[account_id]
                secho(f"Platform: {platform}, Account: {account}, ID: {account_id}", fg="green")
            else:
                secho(f"Unknown account ID: {account_id}", fg="red")

    def all_used_keys(self) -> None:
        used_keys = self.used_db.get_all_used_keys()

        for used_key in used_keys:
            secho(f"Platform: {used_key[0]}, Account: {used_key[1]}, Key: {used_key[2]}", fg="green")

    def update_password(self) -> None:
        current_password = getpass("Enter your current password: ").encode()
        
        # Create a temporary key manager with the current password to verify it
        temp_key_manager = MasterKeyManager(current_password)
        if temp_key_manager.load_master_key() is None:
            secho("Incorrect password", fg="red")
            return

        hide_password = prompt("Hide password? (y/n): ", type=str)

        new_password = []
        for i in range(3):
            if hide_password == "y":
                pwd = getpass(f"Enter password {i+1}: ").encode()
            else:
                pwd = getpass(f"Enter password {i+1}: ")
                secho(f"Password {i+1}: {pwd}", fg="green")
                pwd = pwd.encode()
            new_password.append(pwd)
        self.master_key_manager.update_master_key(new_password)
        secho("Password updated successfully", fg="green")

        
        
        
    

            


    


    
    


