from encryption.crypto_handler import CryptoHandler
from encryption.master_key_manager import MasterKeyManager
from utils.input_handler import InputHandler
from utils.db_utils import DbInit
from utils.db_utils import DBUtils

from sys import exit as sys_exit

from click import secho

from pathlib import Path
from getpass import getpass

def main():
    secho("\n" + "=" * 40, fg="green")
    secho("🔐  Backup Key Manager", fg="green", bold=True, underline=True)
    secho("=" * 40 + "\n", fg="green")

    secho("👋 Welcome to the Backup Key Manager!", fg="green", bold=True)
    secho("🔑 Please enter your master password to continue.", fg="yellow")
    secho("🆕 First-time users should enter a new password.\n", fg="yellow")

    master_password = getpass().encode()
    secho("Please enter your master password again to confirm", fg="yellow")
    confirm_password = getpass().encode()

    if master_password != confirm_password:
        secho("Passwords do not match", fg="red")
        exit(1)
    
    # Initalize Master Key Manager
    key_manager = MasterKeyManager(master_password)

    # Confirm Password
    if not any(Path("keyvault").glob("master_key_*.enc")):
        secho("\nNo master key found. Generating new master key... \n", fg="yellow")
        passwords = []
        for i in range(3):
            pwd = getpass(f"Enter password {i+1}: ").encode()
            passwords.append(pwd)
        master_key = key_manager.generate_master_key(passwords)
        secho("\nMaster key generated successfully! \n", fg="green")
    
    else:
        secho("\nLoading existing master key... \n", fg="yellow")
        master_key = key_manager.load_master_key()
        if master_key:
            secho("\nMaster key loaded successfully! \n", fg="green")
        else:
            secho("\nExiting... Wrong password or master key corrupted - Please try again \n", fg="red", bold=True, underline=True)
            sys_exit(1)

    # Initialize Crypto Handler
    crypto_handler = CryptoHandler(master_password)

    # Initialize DB
    db_dir = Path("db")
    db_init = DbInit(db_dir)
    db_init.initalize_all()

    # Initialize database utilities
    open_db = DBUtils(db_dir / "open_index.db")
    encrypted_db = DBUtils(db_dir / "encrypted_index.db")
    used_db = DBUtils(db_dir / "used_index.db")

    # Initialize Input Handler with required instances
    input_handler = InputHandler(key_manager, crypto_handler, open_db, encrypted_db, used_db)

    while True:
        secho("\nPrint -help for list of commands \n", fg="yellow")
        command = input("Enter a command: ")

        if command in ["-help", "add_account", "add_backup_key", "view_backup_key", 
                       "view_used_key", "delete_used_key", "all_accounts", 
                       "all_backup_keys", "all_used_keys", "update_password", 
                       "exit"]:
            
            if command == "-help":
                input_handler.help()

            if command == "add_account":
                input_handler.add_account()

            if command == "add_backup_key":
                input_handler.add_backup_key()

            if command == "view_backup_key":
                input_handler.view_backup_key()

            if command == "view_used_key":
                input_handler.view_used_key()

            if command == "delete_used_key":
                input_handler.delete_used_key()

            if command == "all_accounts":
                input_handler.all_accounts()

            if command == "all_backup_keys":
                input_handler.all_backup_keys()

            if command == "all_used_keys":
                input_handler.all_used_keys()

            if command == "update_password":
                input_handler.update_password()

            if command == "exit":
                sys_exit(0)
        
        else:
            secho("Invalid command", fg="red")


if __name__ == "__main__":
    main()
        
    

    
    
    
    
    














