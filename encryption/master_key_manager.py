from base64 import b64encode, b64decode
from os import urandom
from typing import Optional, List
from pathlib import Path
from json import load
from click import secho 

from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class MasterKeyManager:
    def __init__(self, password: bytes, encryption_key_dir: Path = Path("keyvault"),config_path: Path = Path("config/settings.json"), master_key_file_pattern: str = "master_key_{}.enc") -> None:
        self.password: bytes = password

        self.encryption_key_dir: Path = encryption_key_dir
        if not self.encryption_key_dir.exists():
            secho(f"Encryption key directory does not exist: {self.encryption_key_dir}", fg="red")
            self.encryption_key_dir.mkdir(exist_ok=True)

        with open(config_path, "r") as f:
            self.config: dict = load(f)
        
        self.salt: bytes = b64decode(self.config["master_key_salt"])
        self.argon2_time_cost: int = self.config["argon2_time_cost"]
        self.argon2_memory_cost: int = self.config["argon2_memory_cost"]
        self.argon2_parallelism: int = self.config["argon2_parallelism"]
        self.argon2_length: int = self.config["argon2_length"]

        self.master_key_file_pattern: str = master_key_file_pattern

    def _derive_key(self, password: Optional[bytes] = None) -> bytes:
        if password is None:
            password = self.password
            
        kdf = Argon2id(
            length=self.argon2_length,
            salt=self.salt,
            iterations=self.argon2_time_cost,
            memory_cost=self.argon2_memory_cost,
            lanes=self.argon2_parallelism
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

            secho(f"Generated and saved master key {i}", fg="green")

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
                secho(f"Error loading master key from {file}: {e}", fg="red")
                continue

        secho("No master key found", fg="red")
        return None
    
    def update_master_key(self, new_password: List[bytes]) -> None:
        if not new_password:
            secho("No new password provided", fg="red")
            return
        
        if len(new_password) != 3:
            secho("Invalid number of passwords provided", fg="red")
            return
        
        current_master_key = self.load_master_key()
        if current_master_key is None:
            secho("Failed to load current master key", fg="red")
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

        secho("Master key updated successfully!", fg="green")
        

