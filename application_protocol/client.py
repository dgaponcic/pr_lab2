from encryption_protocol.client_mixin import ClientMixin 

class Client:
    def __init__(self, client_host, phone_host, phone_port):
        encryption_p = ClientMixin(client_host)
        encryption_p.connect(phone_host, phone_port)
        self.sock = encryption_p

    def pick_phone(self):
        try:
            self.sock.write("Picked Phone")
            response = self.sock.read()
            number = ""

            if response == "Waiting for number":
                print("Introduce the number")
                new_digit = input()

                while new_digit != "Stop":
                    number += new_digit
                    new_digit = input()
                    
            print(number)
        except Exception as e:
            print(e)


    def fileno(self):
        return self.sock.fileno()