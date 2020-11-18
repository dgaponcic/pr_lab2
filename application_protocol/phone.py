from encryption_protocol.server_mixin import ServerMixin

class Phone:
    def __init__(self, host=None, port=None, conn=None):
        if host:
            encryption_p = ServerMixin(host, port)
            self.sock = encryption_p
        else:
            self.sock = conn

    def fileno(self):
        return self.sock.fileno()
    
    def accept(self, host):
        conn = self.sock.accept(host)
        return Phone(conn=conn)

    def receive_number(self):
        try:
            req = self.sock.read()
            if req == "Picked Phone":
                self.sock.write("Waiting for number")
        except Exception as e:
            print(e)
            
