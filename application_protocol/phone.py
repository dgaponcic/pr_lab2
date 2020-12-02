from encryption_protocol.server_mixin import ServerMixin
from encryption_protocol.client_mixin import ClientMixin


class Phone:
  def __init__(self, host, port, phone_lookup):
    self.host = host
    self.sock = ServerMixin(host, port)
    self._client = None
    self._inbound = None
    self._outbound = ClientMixin(host)
    self.active = None
    self.phone_lookup = phone_lookup


  @property
  def inbound(self):
    return self._inbound

  @property
  def outbound(self):
    return self._outbound

  @property
  def client(self):
    return self._client


  def fileno(self):
    return self.sock.fileno()


  def accept(self, host):
    conn = self.sock.accept(host)

    req = conn.read()
    if req == "client connection":
        self._client = conn

    elif req == "incoming call":
      self.incoming_call(conn)

    elif req == "end call":
      self._inbound = None
      self._client.write("call ended")

    return conn


  def incoming_call(self, conn):
    self._client.write("calling")
    answer = self._client.read()
    if answer == "accepted":
        self._inbound = conn
        self.active = self._inbound
        conn.write("accepted")
    else:
        conn.write("rejected")


  def get_number(self):
    number = ""
    recv = self._client.read()
    while recv != "stop":
        number += recv
        recv = self._client.read()
    
    return number


  def call(self, number):
    try:
      addr = self.phone_lookup.get_addr(number)
      self._outbound.connect(addr["host"], addr["port"])
      self.active = self._outbound
      self._outbound.write("incoming call")
    except BlockingIOError:
      self._client.write("an error occured, try later")


  def client_incoming(self):
    data = self._client.read()
    if data == "dialing":
        nb = self.get_number()
        self.call(nb)
    else:
        self.active.write(data)


  def get_reply(self, type=None):
    data = self.active.read()

    if type == "client" and data == "rejected":
        self._client.write("call rejected")

    elif type == "client" and data == "accepted":
        self._client.write("call accepted")  

    elif data == "end call":
      self._inbound = None
      self._client.write("call ended")  

    else:
        self._client.write(data)
