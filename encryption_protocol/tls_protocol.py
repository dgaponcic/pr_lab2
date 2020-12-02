from encryption_protocol.key_generation_math import generate_public_keys, generate_private, calculate_key
from encryption_protocol.encryption import Encryption
import transport_protocol.protocol as p
import random


class ProtocolTLS:
  def __init__(self, sock):
    self.sock = sock


  def read_g_p_keys(self, sock):
    public_key_p = int(p.read(sock))
    public_key_g = int(p.read(sock))

    return public_key_g, public_key_p


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


  def generate_key(self, min_nb, max_nb):
    return random.randint(min_nb, max_nb)


  def read(self):
    receiver = self.sock
    val = p.read(receiver).encode("utf-8")

    return self.encryption.decrypt_data(val)


  def write(self, val):
    try:
      sender = self.sock
      val2 = self.encryption.encrypt_data(val)
      p.write(val2.decode("utf-8"), sender)
    except Exception as e:
      raise e


  def fileno(self):
    return self.sock.fileno()
