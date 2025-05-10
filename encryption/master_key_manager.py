from base64 import b64encode, b64decode
from os import urandom
from typing import Optional, List
from pathlib import Path
from json import load

from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class MasterKeyManager:
    def __init__(self, password: bytes, encryption_key_dir: Path = Path("keyvault"),config_path: Path = Path("config/settings.json")) -> None:
        self.password: bytes = password

        self.encryption_key_dir: Path = encryption_key_dir
        if not self.encryption_key_dir.exists():
            print(f"Encryption key directory does not exist: {self.encryption_key_dir}")
            self.encryption_key_dir.mkdir(exist_ok=True)

        with open(config_path, "r") as f:
            self.config: dict = load(f)
        
        self.salt: bytes = b64decode(self.config["master_key_salt"])
        self.master_key_file_pattern = self.config["master_key_file_pattern"]

    def _derive_key(self, password: Optional[bytes] = None) -> bytes:
        if password is None:
            password = self.password
            
        kdf = Argon2id(
            length=self.config["argon2_length"],
            salt=self.salt,
            iterations=self.config["argon2_time_cost"],
            memory_cost=self.config["argon2_memory_cost"],
            lanes=self.config["argon2_parallelism"]
        )
        return kdf.derive(password)
    
    def generate_master_key(self, all_passwords: List[bytes]) -> bytes:
        master_key: bytes = urandom(32)

        for i, password in enumerate(all_passwords):
 
            key: bytes = self._derive_key(password)
            aesgcm: AESGCM = AESGCM(key)
            nonce: bytes = urandom(12)
            ciphertext: bytes = aesgcm.encrypt(nonce, master_key, associated_data=None)
            encrypted_key: bytes = b64encode(nonce + ciphertext)
            
            key_file_path: Path = self.encryption_key_dir / self.master_key_file_pattern.format(i)
            with open(key_file_path, "wb") as f:
                f.write(encrypted_key)

            print(f"Generated and saved master key {i}")

        return master_key
    
    def load_master_key(self) -> Optional[bytes]:
        key = self._derive_key()
        aesgcm: AESGCM = AESGCM(key)

        for file in self.encryption_key_dir.glob(self.master_key_file_pattern.format("*")):
            try:
                with open(file, "rb") as f:
                    encrypted_key: bytes = b64decode(f.read())

                nonce: bytes = encrypted_key[:12]
                ciphertext: bytes = encrypted_key[12:]

                return aesgcm.decrypt(nonce, ciphertext, associated_data=None)
            except Exception as e:
                print(f"Error loading master key from {file}: {e}")
                continue

        print("No master key found")
        return None
    
    def update_master_key(self, new_password: List[bytes]) -> None:
        if not new_password:
            print("No new password provided")
            return
        
        if len(new_password) != 3:
            print("Invalid number of passwords provided")
            return
        
        current_master_key = self.load_master_key()
        if current_master_key is None:
            print("Failed to load current master key")
            return
        
        for i, password in enumerate(new_password):
            key: bytes = self._derive_key(password)
            aesgcm: AESGCM = AESGCM(key)
            nonce: bytes = urandom(12)
            ciphertext: bytes = aesgcm.encrypt(nonce, current_master_key, associated_data=None)
            encrypted_key: bytes = b64encode(nonce + ciphertext)
            
            key_file_path: Path = self.encryption_key_dir / self.master_key_file_pattern.format(i)
            with open(key_file_path, "wb") as f:
                f.write(encrypted_key)

        print("Master key updated successfully!")
        

if __name__ == "__main__":
    from getpass import getpass
    from pathlib import Path
    from json import load


    config_path = Path("config/settings.json")
    with open(config_path) as f:
        config = load(f)
    
    password = getpass("Enter master password: ").encode()
    key_manager = MasterKeyManager(password)

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
        key_manager._derive_key()
        master_key = key_manager.load_master_key()
        if master_key:
            print("Master key loaded successfully!")
        else:
            print("Failed to load master key")

