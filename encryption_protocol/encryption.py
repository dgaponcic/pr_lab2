from cryptography.fernet import Fernet
import base64

class Encryption:

  def __init__(self, key):
    key = base64.urlsafe_b64encode(key.to_bytes(32, "big"))
    self.cryptor = Fernet(key)

  def encrypt_data(self, data):
    return self.cryptor.encrypt(data.encode())

  def decrypt_data(self, data):
    return self.cryptor.decrypt(data).decode()
    