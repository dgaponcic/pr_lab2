from application_protocol.client import Client

HOST = "127.0.0.1"

if __name__ == "__main__": 
    client = Client(HOST, HOST, 10000)
    client.pick_phone()
