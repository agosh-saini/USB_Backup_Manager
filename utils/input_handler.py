from typing import Optional, Tuple, List
from click import prompt, confirm
from getpass import getpass

class InputHandler:
    def __init__(self) -> None:
        pass
    
    def prompt_confirm(self) -> Optional[bool]:
        return confirm("Are you sure you want to continue? ")
    
    def prompt_confirm_twice(self) -> bool:
        first = confirm("Are you sure you want to continue? ")
        if not first:
            return False
        second = confirm("Please confirm again. Are you really sure?")
        return second
    
    def prompt_with_cancel(self, message: str, allow_cancel: bool = True) -> Optional[str]:
        val = prompt(f"{message} (or type 'cancel' to abort)")
        return None if allow_cancel and val.lower() == "cancel" else val
    
    def get_password(self) -> Optional[str]:
        return getpass("Enter the password: ")

    def prompt_set_password(self) -> Optional[str]:
        return getpass("Enter the new password: ")

    def prompt_confirm_password(self) -> Optional[str]:
        return getpass("Confirm the new password: ")

    def prompt_account_info(self) -> Tuple[str, str]:
        platform = prompt("Enter the platform: ")
        account_name = prompt("Enter the account name: ")
        return platform, account_name
    
    def print_account_summary(self, platform: Optional[str], account_name: Optional[str], key_count: Optional[int]) -> None:
        print(f"Platform: {platform}")
        print(f"Account Name: {account_name}")
        print(f"Key Count: {key_count}")
    

    def print_backup_key_table(self, backup_key_table: list[tuple[str, str]]) -> None:
        print(f"Account ID\tEncrypted Key")
        for account_id, encrypted_key in backup_key_table:
            print(f"{account_id}\t{encrypted_key}")

    def show_used_key_table(self, used_key_table: List[Tuple[str, str, str]]) -> None:
        print(f"Platform\tAccount Name\tUsed Key")
        for platform, account_name, used_key in used_key_table:
            print(f"{platform}\t{account_name}\t{used_key}")

    def return_backup_key(self, platform: Optional[str], account_name: Optional[str], backup_key: Optional[str]) -> Optional[str]:
        print(f'Backup key for {platform} - {account_name}: {backup_key}')
        return backup_key
    
    def return_used_key(self, platform: Optional[str], account_name: Optional[str], used_key: Optional[str]) -> Optional[str]:
        print(f'Used key for {platform} - {account_name}: {used_key}')
        return used_key

    def prompt_backup_keys(self) -> list[str]:
        raw = prompt("Enter comma-separated backup keys: ")
        return [k.strip() for k in raw.split(",") if k.strip()]
    
    def select_from_list(self, label: str, options: list[str]) -> str:
        print(label)
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        choice = int(prompt("Choose an option number: "))
        return options[choice - 1]

            


    


    
    


