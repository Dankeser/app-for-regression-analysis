from cryptography.fernet import Fernet
import hashlib
import base64
import json
import hmac

def hash_password(password: str) -> str:
    password = password.encode()
# here does not have to be a key that contains anything outside of ascii characters.
    h = hmac.new( b'meingeheimeschlussel',b'', hashlib.sha3_512)
    h.update(password)
    return h.hexdigest()


class EncryptClass:
        @staticmethod
        def my_key_generator(chiffre: str) -> bytes:
                # summary of chiffre with hashfunction
                key = chiffre.encode().ljust(32, b'\0')[:32]
                key = base64.urlsafe_b64encode(key)
                return key

        # Erhält Python-Objekt, gibt verschlüsselte string.
        def encrypt_function(self, content_to_encrypt: object) -> str:
                self.cipher_suite = Fernet(self.user_instance.user_key)
                return self.cipher_suite.encrypt(json.dumps(content_to_encrypt).encode()).decode()

        # Erhält verschlüsselte string, gibt Python-Objekt zurück.
        def decrypt_function(self, content_to_decrypt: str) -> object:
                self.cipher_suite = Fernet(self.user_instance.user_key)
                return json.loads(self.cipher_suite.decrypt(json.dumps(content_to_decrypt).encode()).decode())