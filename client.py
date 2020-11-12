from encryption_protocol.client_mixin import ClientMixin 
import socket

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
