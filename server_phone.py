from application_protocol.phone import Phone
import selectors
import traceback

sel = selectors.DefaultSelector()
HOST = "127.0.0.1"
PORT = 10000

if __name__ == "__main__":
    phone = Phone(HOST, PORT)
    sel.register(phone, selectors.EVENT_READ, data=None)

    while True:
        try:
            readable = sel.select(timeout=None)
            for key, _ in readable:
                if key.fileobj == phone:
                    # print("here")
                    new_conn = phone.accept(HOST)
                    sel.register(new_conn, selectors.EVENT_READ, data=None)
                    # phone.receive_number()
                else:
                    key.fileobj.receive_number()
                #     request = key.fileobj.read()
                #     print("read req", request)
                #     res = request + " HEHE"
                #     key.fileobj.write(res)
        except Exception as e:
            print(e)
            pass