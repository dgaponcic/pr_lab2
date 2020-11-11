import socket
from tls_protocol import ProtocolTLS

HOST = "127.0.0.1"
SERVER_PORT = 10000

if __name__ == "__main__":
  p_tls = ProtocolTLS(HOST, 0)
  sock = p_tls.sock
  p_tls.connect(sock, HOST, SERVER_PORT)

  while True:
    payload = input("Your payload: ")
    p_tls.write(payload, sock)
    response = p_tls.read(sock)
    print("response:", response)
