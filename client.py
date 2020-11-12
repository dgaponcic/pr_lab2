import socket
# from encryption_protocol.tls_protocol import ProtocolTLS
from encryption_protocol.client_mixin import ClientMixin 

HOST = "127.0.0.1"
SERVER_PORT = 10000

if __name__ == "__main__":
  encryption_p = ClientMixin(HOST)
  encryption_p.connect(HOST, SERVER_PORT)

  while True:
    payload = input("Your payload: ")
    encryption_p.write(payload)
    response = encryption_p.read()
    print("response:", response)
