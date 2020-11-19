from application_protocol.phone import Phone
import select
import sys

HOST = "127.0.0.1"
PORT = int(sys.argv[1])

if __name__ == "__main__":
    phone = Phone(HOST, PORT)
    inputs = [ phone, phone.phone_client ]
    outputs = [ ]

    while True:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        
        for readable in readable:
            if readable == phone and (not phone.phone_server or not phone.client):
                conn = phone.accept(HOST)
                inputs.append(conn)
            
            elif readable == phone.client:
                phone.client_incoming()


            elif readable == phone.phone_server:
                phone.get_reply()
            
            elif readable == phone.phone_client:
                phone.get_reply()

