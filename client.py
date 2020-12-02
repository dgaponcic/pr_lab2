from application_protocol.client import Client
import sys

HOST = "127.0.0.1"
PHONE_PORT = int(sys.argv[1])

def state_dialing(client):
  client.pickup()
  ans = client.get_reply()
  print(ans)
  if ans == "accepted": 
    while True:
      data = input("")
      client.reply(data)
      if data == "end call":
        return 
      recv = client.get_reply()
      print(recv)
  elif ans == "rejected":
    print("Your call was rejected")

def state_idle(client):
  rcv = client.get_reply()
  if rcv == "calling":
    answer = input("Calling, do you want to answer? ")
    if answer == "y":
      client.reply("accepted")
      while True:
        reply = client.get_reply()
        print(reply)
        if reply == "call ended":
          break
        data = input("")
        client.reply(data)
    else:
      client.reply("rejected")

def dispatch_states(client):
  while True:
    state = input("state: ")
    if state == "dialing":
      state_dialing(client)
    elif state == "idle":
      state_idle(client)
    

if __name__ == "__main__":
  client = Client(phone_host=HOST, phone_port=PHONE_PORT, client_host=HOST)
  dispatch_states(client)
        