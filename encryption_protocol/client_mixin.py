from encryption_protocol.tls_protocol import ProtocolTLS
from encryption_protocol.encryption import Encryption
import transport_protocol.protocol as p


class ClientMixin(ProtocolTLS):
  
  def __init__(self, host, port = 0):
    self.sock = p.init(host, port)


  def connect(self, host, port):
    sock = self.sock
    p.connect(sock, host, port)
    p.write("TLS", sock)
    key = self.get_client_key(sock)
    print(key)
    self.encryption = Encryption(key)
