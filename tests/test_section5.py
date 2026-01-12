import unittest
import shutil
import os
from pathlib import Path
import sys

# Fix path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.security.encryption import SecurityManager
from core.config import DATA_DIR, ENABLE_ENCRYPTION

class TestSection5(unittest.TestCase):
    def test_encryption_flow(self):
        print("\nTesting Encryption...")
        if not ENABLE_ENCRYPTION:
            print("Encryption disabled in config. Skipping.")
            return

        sm = SecurityManager()
        
        # Create Dummy File
        test_file = DATA_DIR / "secret_doc.txt"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        original_content = b"This is top secret data."
        
        with open(test_file, "wb") as f:
            f.write(original_content)
            
        print(f"Created {test_file}")
        
        # Encrypt
        enc_path = sm.encrypt_file(test_file)
        self.assertIsNotNone(enc_path)
        self.assertTrue(enc_path.exists())
        self.assertTrue(str(enc_path).endswith(".enc"))
        self.assertFalse(test_file.exists(), "Original file should be deleted.")
        
        # Verify content is scrambled
        with open(enc_path, "rb") as f:
            scrambled = f.read()
        self.assertNotEqual(original_content, scrambled)
        print("File encrypted and scrambled.")
        
        # Decrypt
        decrypted = sm.decrypt_data(enc_path)
        self.assertEqual(original_content, decrypted)
        print("Decryption successful.")
        
        # Clean up
        os.remove(enc_path)

if __name__ == '__main__':
    unittest.main()
