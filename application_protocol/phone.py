from encryption_protocol.server_mixin import ServerMixin
from encryption_protocol.client_mixin import ClientMixin

spravocinic = {"0010": {"host": "127.0.0.1", "port": 10001}}

class Phone:
    def __init__(self, host, port):
        self.sock = ServerMixin(host, port)
        self.client = None
        self.phone_server = None
        self.phone_client = ClientMixin(host)
        self.active = None

    def fileno(self):
        return self.sock.fileno()

    def accept(self, host):
        conn = self.sock.accept(host)

        req = conn.read()
        if req == "client connection":
            self.client = conn

        elif req == "incoming call":
            self.client.write(f"calling")
            answer = self.client.read()
            if answer == "accepted":
                self.phone_server = conn
                self.active = self.phone_server
                conn.write("accepted")
            else:
                conn.write("rejected")

        return conn

    def get_number(self):
        number = ""
        recv = self.client.read()
        while recv != "stop":
            number += recv
            recv = self.client.read()
        
        return number

    def call(self, number):
        addr = spravocinic[number]
        self.phone_client.connect(addr["host"], addr["port"])
        self.active = self.phone_client
        self.phone_client.write("incoming call")

    def client_incoming(self):
        data = self.client.read()
        if data == "dialing":
            nb = self.get_number()
            self.call(nb)
        else:
            self.active.write(data)

    def get_reply(self, type=None):
        data = self.active.read()

        if type == "client" and data == "rejected":
            self.client.write("call rejected")
        elif type == "client" and data == "accepted":
            self.client.write("call accepted")
        
        else:
            self.client.write(data)

