from encryption.crypto_handler import CryptoHandler
from encryption.master_key_manager import MasterKeyManager
from utils.input_handler import InputHandler
from utils.db_utils import DbInit
from utils.db_utils import DBUtils

import sys
import os

from pathlib import Path
from getpass import getpass

def main():
    print("Welcome to the Backup Key Manager")
    print("Please enter your master password to continue")
    master_password = getpass().encode()
    print("Please enter your master password again to confirm")
    confirm_password = getpass().encode()

    if master_password != confirm_password:
        print("Passwords do not match")
        sys.exit(1)
    
    # Initalize Master Key Manager
    key_manager = MasterKeyManager(master_password)

    # Confirm Password
    if not any(Path("keyvault").glob("master_key_*.enc")):
        print("No master key found. Generating new master key...")
        passwords = []
        for i in range(3):
            pwd = getpass(f"Enter password {i+1}: ").encode()
            passwords.append(pwd)
        master_key = key_manager.generate_master_key(passwords)
        print("Master key generated successfully!")
    
    else:
        print("Loading existing master key...")
        master_key = key_manager.load_master_key()
        if master_key:
            print("Master key loaded successfully!")
        else:
            print("Failed to load master key")
            sys.exit(1)

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
        print("Print -h for list of commands")
        command = input("Enter a command: ")

        if command in ["-h", "add_account", "add_backup_key", "view_backup_key", 
                       "view_used_key", "delete_used_key", "all_accounts", 
                       "all_backup_keys", "all_used_keys", "update_password", 
                       "exit"]:
            
            if command == "-h":
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
                sys.exit(0)
        
        else:
            print("Invalid command")

   


if __name__ == "__main__":
    main()
        
    
    
    
    
    
    
    
    
    
    














