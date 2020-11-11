import socket
import selectors
import protocolv2 as p
from tls_protocol import ProtocolTLS

sel = selectors.DefaultSelector()
HOST = "127.0.0.1"

if __name__ == "__main__":
  ssl_p = ProtocolTLS(HOST, 10000)
  sel.register(ssl_p.sock, selectors.EVENT_READ, data=None)

  while True:
    try:
      readable = sel.select(timeout=None)
      for key, _ in readable:
        if key.fileobj == ssl_p.sock:
          new_conn = ssl_p.accept(ssl_p.sock, HOST)
          sel.register(new_conn, selectors.EVENT_READ, data=None)
        else:
          request = ssl_p.read(key.fileobj)
          print("read req", request)
          res = request + " HEHE"
          ssl_p.write(res, key.fileobj)
    except Exception as e:
      pass
