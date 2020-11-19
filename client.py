from application_protocol.client import Client
import sys

HOST = "127.0.0.1"
PHONE_PORT = int(sys.argv[1])

if __name__ == "__main__":
    client = Client(HOST, HOST, PHONE_PORT)
    while True:
        state = input("state: ")
        if state == "dialing":
            client.pickup()
            ans = client.get_reply()
            print(ans)
            if ans == "accepted": 
                while True:
                    data = input("")
                    client.reply(data)
                    recv = client.get_reply()
                    print(recv)
            elif ans == "rejected":
                print("Your call was rejected")

        if state == "idle":
            rcv = client.get_reply()
            if rcv == "calling":
                answer = input("Calling, do you want to answer? ")
                if answer == "y":
                    client.reply("accepted")
                    while True:
                        reply = client.get_reply()
                        print(reply)
                        data = input("")
                        client.reply(data)
                else:
                    client.reply("rejected")
            