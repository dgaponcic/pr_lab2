from encryption_protocol.server_mixin import ServerMixin
import selectors
import socket
import sys

sel = selectors.DefaultSelector()
HOST = "0.0.0.0"
PORT = 10000

if __name__ == "__main__":
  encryption_p = ServerMixin(HOST, PORT)
  sel.register(encryption_p, selectors.EVENT_READ, data=None)

  while True:
    readable = sel.select(timeout=None)
    for key, _ in readable:
      if key.fileobj == encryption_p:
        new_conn = encryption_p.accept(HOST)
        sel.register(new_conn, selectors.EVENT_READ, data=None)
      else:
        request = key.fileobj.read()
        print("read req", request)
        res = f"received {request}"
        key.fileobj.write(res)
