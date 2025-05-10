from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import List, Optional
from os import urandom
from encryption.master_key_manager import MasterKeyManager
from click import secho

class CryptoHandler:
    def __init__(self, password: bytes, config_path: str = "config/settings.json") -> None:
        self.key_manager = MasterKeyManager(password, config_path=config_path)
        self.master_key = self.key_manager.load_master_key()
        if not self.master_key:
            secho("\nFailed to load master key \n", fg="red")
            raise ValueError("Failed to load master key")

    def encrypt(self, data: bytes) -> str:
        aesgcm: AESGCM = AESGCM(self.master_key)
        nonce: bytes = urandom(12)
        ciphertext: bytes = aesgcm.encrypt(nonce, data, associated_data=None)
        return b64encode(nonce + ciphertext).decode()
    
    def decrypt(self, encrypted_data: str) -> Optional[bytes]:
        try:
            encrypted_data: bytes = b64decode(encrypted_data)
            nonce: bytes = encrypted_data[:12]
            ciphertext: bytes = encrypted_data[12:]

            aesgcm: AESGCM = AESGCM(self.master_key)
            return aesgcm.decrypt(nonce, ciphertext, associated_data=None)
        except Exception as e:
            secho(f"\nError decrypting data: {e} \n", fg="red")
            return None
