from encryption_protocol.tls_protocol import ProtocolTLS
from encryption_protocol.encryption import Encryption
import transport_protocol.protocolv2 as p


class ServerMixin(ProtocolTLS):

  def __init__(self, host, port = 0):
    self.sock = p.init(host, port)


  def accept(self, host):
    new_sock = p.accept(self.sock, host)
    new_tls_sock = ProtocolTLS(new_sock)
    req = p.read(new_sock)
    if req == "TLS":
      key = new_tls_sock.get_server_key(new_sock)
      print(key)
      new_tls_sock.encryption = Encryption(key)

      return new_tls_sock