from encryption_protocol.server_mixin import ServerMixin
import selectors
import socket

sel = selectors.DefaultSelector()
HOST = "127.0.0.1"
PORT = 10000

if __name__ == "__main__":
  encryption_p = ServerMixin(HOST, PORT)
  sel.register(encryption_p, selectors.EVENT_READ, data=None)

  while True:
    try:
      readable = sel.select(timeout=None)
      for key, _ in readable:
        if key.fileobj == encryption_p:
          new_conn = encryption_p.accept(HOST)
          sel.register(new_conn, selectors.EVENT_READ, data=None)
        else:
          request = key.fileobj.read()
          print("read req", request)
          res = request + " HEHE"
          key.fileobj.write(res)
    except Exception as e:
      pass
