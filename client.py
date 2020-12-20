from encryption_protocol.client_mixin import ClientMixin 
import socket

HOST = "0.0.0.0"
SERVER_PORT = 10000

if __name__ == "__main__":
  encryption_p = ClientMixin(HOST)
  encryption_p.connect("server", SERVER_PORT)

  while True:
    try:
      payload = input("Your payload: ")
      encryption_p.write(payload)
      response = encryption_p.read()
      print("response:", response)
    except Exception as e:
      print(e)
      pass
