from encryption.crypto_handler import CryptoHandler, MasterKeyManager
from getpass import getpass
from pathlib import Path
from json import load


def test_encryption():
    config_path = Path("config/settings.json")
    with open(config_path) as f:
        config = load(f)
    
    password = getpass("Enter master password: ").encode()
    key_manager = MasterKeyManager(password)


    print("Loading existing master key...")
    key_manager._derive_key()
    master_key = key_manager.load_master_key()
    if master_key:
        print("Master key loaded successfully!")
    else:
        print("Failed to load master key")

    crypto_handler = CryptoHandler(password)

    data = b"Hello, World!"
    encrypted_data = crypto_handler.encrypt(data)
    print(f"Encrypted data: {encrypted_data}")

    decrypted_data = crypto_handler.decrypt(encrypted_data)
    print(f"Decrypted data: {decrypted_data}")

    assert decrypted_data == data


if __name__ == "__main__":
    test_encryption()



