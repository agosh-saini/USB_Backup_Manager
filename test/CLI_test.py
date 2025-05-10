from utils.input_handler import InputHandler

def run_tests():
    handler = InputHandler()

    print("\n--- Testing prompt_account_info ---")
    platform, account_name = handler.prompt_account_info()
    print(f"Received: platform={platform}, account_name={account_name}")

    print("\n--- Testing prompt_backup_keys ---")
    keys = handler.prompt_backup_keys()
    print(f"Received keys: {keys}")

    print("\n--- Testing prompt_confirm ---")
    if handler.prompt_confirm():
        print("Confirmed.")
    else:
        print("Not confirmed.")

    print("\n--- Testing prompt_confirm_twice ---")
    if handler.prompt_confirm_twice():
        print("Double confirmed.")
    else:
        print("Canceled.")

    print("\n--- Testing get_password ---")
    pw = handler.get_password()
    print(f"Password received: {'*' * len(pw)}")

    print("\n--- Testing print_account_summary ---")
    handler.print_account_summary(platform, account_name, key_count=5)

    print("\n--- Testing print_backup_key_table ---")
    handler.print_backup_key_table([("acc123", "encryptedkey1=="), ("acc456", "encryptedkey2==")])

    print("\n--- Testing show_used_key_table ---")
    handler.show_used_key_table([
        ("Gmail", "john@example.com", "usedkey1"),
        ("GitHub", "dev@example.com", "usedkey2")
    ])

    print("\n--- Testing return_backup_key ---")
    backup_key = handler.return_backup_key(platform, account_name, "backupkey1")
    print(f"Entered backup key: {backup_key}")

    print("\n--- Testing return_used_key ---")
    used_key = handler.return_used_key(platform, account_name, "usedkey1")
    print(f"Entered used key: {used_key}")

if __name__ == "__main__":
    run_tests()
