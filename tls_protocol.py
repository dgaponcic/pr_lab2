from cryptography.fernet import Fernet
from encryption import Encryption
import protocolv2 as p
import random
from generate_math import generate_public_keys, generate_private, calculate_key


class ProtocolTLS:
  def __init__(self, host, port):
    self.sock = p.init(host, port)

  def read_g_p_keys(self, sock):
    public_key_p = int(p.read(sock))
    public_key_g = int(p.read(sock))
    return public_key_g, public_key_p
    

  def accept(self, sock, host):
    new_sock = p.accept(sock, host)
    req = p.read(new_sock)
    if req == "TLS":
      key = self.get_server_key(new_sock)
      self.encryption = Encryption(key)
      return new_sock


  def get_client_key(self, sock):
    public_key_g, public_key_p = self.read_g_p_keys(sock)
    private = generate_private(1, 1000)
    sender_public_key = calculate_key(public_key_g, public_key_p, private)
    p.write(str(sender_public_key), sock)
    receiver_public_key = int(p.read(sock))
    
    return calculate_key(receiver_public_key, public_key_p, private)


  def get_server_key(self, sock):
    public_key_p, public_key_g = generate_public_keys(1, 1000)
    p.write(str(public_key_p), sock)
    p.write(str(public_key_g), sock)
    private = generate_private(1, 1000)
    public_key_generated = calculate_key(public_key_g, public_key_p, private)
    public_key_generated2 = int(p.read(sock))
    p.write(str(public_key_generated), sock)

    return calculate_key(public_key_generated2, public_key_p, private)


  def connect(self, sock, host, port):
    p.connect(sock, host, port)
    p.write("TLS", sock)
    key = self.get_client_key(sock)
    print(key)
    self.encryption = Encryption(key)


  def generate_key(self, min_nb, max_nb):
    return random.randint(min_nb, max_nb)


  def read(self, receiver):
    val = p.read(receiver).encode("utf-8")
    return self.encryption.decrypt_data(val)


  def write(self, val, sender):
    val2 = self.encryption.encrypt_data(val)
    p.write(val2.decode("utf-8"), sender)
