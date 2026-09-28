from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
try:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
except ImportError:
    PBKDF2 = None
from cryptography.hazmat.backends import default_backend
import base64
import os
import hashlib

class CryptoManager:
    """Manages encryption and decryption operations"""
    
    @staticmethod
    def generate_salt(length: int = 16) -> bytes:
        """Generate a random salt"""
        return os.urandom(length)
    
    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        try:
            if PBKDF2 is not None:
                kdf = PBKDF2(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                    backend=default_backend()
                )
                key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
                return key
            else:
                raise ImportError("PBKDF2 not available")
        except Exception as e:
            # Fallback for different cryptography versions
            # Use simpler key derivation
            combined = (password + base64.b64encode(salt).decode()).encode()
            hash_obj = hashlib.pbkdf2_hmac('sha256', combined, salt, 100000)
            key = base64.urlsafe_b64encode(hash_obj[:32])
            return key
    
    @staticmethod
    def encrypt_file(file_content: bytes, password: str) -> bytes:
        """
        Encrypt file content using AES-256 (via Fernet)
        
        Args:
            file_content: Raw bytes of the file
            password: Encryption password
        
        Returns:
            Encrypted file content with salt prepended
        """
        try:
            # Generate random salt
            salt = CryptoManager.generate_salt()
            
            # Derive key from password and salt
            key = CryptoManager.derive_key(password, salt)
            
            # Create Fernet cipher
            cipher = Fernet(key)
            
            # Encrypt the file content
            encrypted_content = cipher.encrypt(file_content)
            
            # Prepend salt to encrypted content (salt is not secret)
            # Format: [16 bytes salt][encrypted content]
            result = salt + encrypted_content
            
            return result
        
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    @staticmethod
    def decrypt_file(encrypted_content: bytes, password: str) -> bytes:
        """
        Decrypt file content
        
        Args:
            encrypted_content: Encrypted file content (with salt prepended)
            password: Decryption password
        
        Returns:
            Decrypted file content
        """
        try:
            # Extract salt from encrypted content (first 16 bytes)
            salt = encrypted_content[:16]
            encrypted_data = encrypted_content[16:]
            
            # Derive key from password and salt
            key = CryptoManager.derive_key(password, salt)
            
            # Create Fernet cipher
            cipher = Fernet(key)
            
            # Decrypt the content
            decrypted_content = cipher.decrypt(encrypted_data)
            
            return decrypted_content
        
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")


class HashManager:
    """Manages file hashing"""
    
    @staticmethod
    def hash_file(file_content: bytes, algorithm: str = 'sha256') -> str:
        """
        Generate hash of file content
        
        Args:
            file_content: Raw bytes of the file
            algorithm: Hash algorithm (sha256, sha512, md5)
        
        Returns:
            Hexadecimal hash string
        """
        try:
            if algorithm == 'sha256':
                hasher = hashlib.sha256()
            elif algorithm == 'sha512':
                hasher = hashlib.sha512()
            elif algorithm == 'md5':
                hasher = hashlib.md5()
            else:
                hasher = hashlib.sha256()
            
            hasher.update(file_content)
            return hasher.hexdigest()
        
        except Exception as e:
            raise Exception(f"Hashing failed: {str(e)}")


# Export functions
def encrypt_file(file_content: bytes, password: str) -> bytes:
    """Encrypt file content"""
    return CryptoManager.encrypt_file(file_content, password)


def decrypt_file(encrypted_content: bytes, password: str) -> bytes:
    """Decrypt file content"""
    return CryptoManager.decrypt_file(encrypted_content, password)


def hash_file(file_content: bytes) -> str:
    """Generate hash of file"""
    return HashManager.hash_file(file_content)


def verify_password_strength(password: str) -> tuple[bool, str]:
    """
    Verify password strength
    
    Returns:
        (is_strong, message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    strength = sum([has_upper, has_lower, has_digit, has_special])
    
    if strength >= 3:
        return True, "Strong password"
    elif strength == 2:
        return True, "Medium strength password"
    else:
        return True, "Weak password - consider adding more variety"
