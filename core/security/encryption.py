import os
from pathlib import Path
from cryptography.fernet import Fernet
from ..config import DATA_DIR
from ..utils import log

class SecurityManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecurityManager, cls).__new__(cls)
            cls._KeyPath = DATA_DIR / "secret.key"
            cls._instance._load_or_create_key()
        return cls._instance

    def _load_or_create_key(self):
        if self._KeyPath.exists():
            with open(self._KeyPath, "rb") as key_file:
                self.key = key_file.read()
        else:
            self.key = Fernet.generate_key()
            try:
                with open(self._KeyPath, "wb") as key_file:
                    key_file.write(self.key)
                log.warning(f"New Encryption Key generated at {self._KeyPath}. DO NOT LOSE THIS.")
            except Exception as e:
                log.error(f"Failed to save encryption key: {e}")
                
        self.fernet = Fernet(self.key)

    def encrypt_file(self, file_path: Path):
        """
        Encrypts a file in place. Appends .enc extension.
        """
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            
            encrypted = self.fernet.encrypt(data)
            
            enc_path = file_path.with_suffix(file_path.suffix + ".enc")
            with open(enc_path, "wb") as f:
                f.write(encrypted)
            
            # Secure delete original
            os.remove(file_path)
            return enc_path
        except Exception as e:
            log.error(f"Encryption failed for {file_path}: {e}")
            return None

    def decrypt_data(self, file_path: Path) -> bytes:
        """
        Returns decrypted bytes from an .enc file.
        """
        try:
            with open(file_path, "rb") as f:
                encrypted = f.read()
            return self.fernet.decrypt(encrypted)
        except Exception as e:
            log.error(f"Decryption failed for {file_path}: {e}")
            return None
