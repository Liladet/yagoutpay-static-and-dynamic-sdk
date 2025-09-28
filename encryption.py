# src/encryption.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

class EncryptionUtils:
    IV = b"0123456789abcdef"  # Static IV from docs

    @staticmethod
    def encrypt(text: str, key: str) -> str:
        key_bytes = base64.b64decode(key)
        padder = padding.PKCS7(128).padder()
        padded_text = padder.update(text.encode()) + padder.finalize()
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(EncryptionUtils.IV), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_text) + encryptor.finalize()
        return base64.b64encode(encrypted).decode()

    @staticmethod
    def decrypt(encrypted_text: str, key: str) -> str:
        key_bytes = base64.b64decode(key)
        encrypted_bytes = base64.b64decode(encrypted_text)
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(EncryptionUtils.IV), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_decrypted = decryptor.update(encrypted_bytes) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted = unpadder.update(padded_decrypted) + unpadder.finalize()
        return decrypted.decode()