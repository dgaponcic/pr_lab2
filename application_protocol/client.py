from encryption_protocol.client_mixin import ClientMixin 

class Client:
    def __init__(self, phone_host, phone_port, client_host, client_port=0):
        encryption_p = ClientMixin(client_host, client_port)
        encryption_p.connect(phone_host, phone_port)
        encryption_p.write("client connection")
        self.sock = encryption_p
    
    def pickup(self):
        self.sock.write("dialing")
        number = ""
        digit = input("Introduce the digit: ")
        while digit != "stop":
            self.sock.write(digit)
            digit = input("Next digit: ")
        self.sock.write("stop")

    def reply(self, msg):
        self.sock.write(msg)
    
    def get_reply(self):
        return self.sock.read()
