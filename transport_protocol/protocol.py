from transport_protocol.request_handler import is_valid, make_payload, get_payload, get_nack_index
from transport_protocol.socket_wrapper import SocketWrapper
import socket
import random
import time

def init(host, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((host, port))

  return SocketWrapper(sock, None)


def connect(sock, host, port):
  sock.sendto(b'SYN', (host, port))
  response, addr = sock.recvfrom(1024)

  if response == b"OK":
    sock.connection = addr
    

def accept(sock, host):
  data, sender = sock.recvfrom(1024)

  if data == b'SYN':
    new_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_conn.bind((host, 0))
    new_conn.sendto( b'OK', sender)

    return SocketWrapper(new_conn, sender)


def read(receiver):
  total_len = -1
  received = []

  while True:
    if len(received) == total_len:
      return join_chunks(received)

    raw_payload, addr = receiver.recvfrom(1024)
    data, index = get_payload(raw_payload)
    
    if is_valid(raw_payload) and random.random() > 0.3:
      receiver.sendto(f'ACK|{index}'.encode("utf-8"), addr)
      print("sending ack")
      if index == 0:
        total_len = int(data)
      else:
        received.append((data, index))
    else:
      receiver.sendto(f'NACK|{index}'.encode("utf-8"), addr)
      print("sending nack")


def write(val, sender):
  receiver = sender.connection
  msgs = split2chunks(val)
  data2send = create_packets(msgs)

  window = 1
  pointer = 0
  waiting = 0
  tresh = 6

  while pointer < len(data2send) or waiting != 0:
    print("window value: " + str(window))
    while waiting < window and pointer < len(data2send):
      sender.sendto(data2send[pointer], receiver)
      waiting += 1
      pointer += 1

    try:
      while True:
          payload, addr = sender.recvfrom(1024, socket.MSG_DONTWAIT)
          if b"NACK" in payload:
            index = get_nack_index(payload)
            sender.sendto(data2send[index], receiver)
            window *= 2 / 3

          elif b"ACK" in payload:
            waiting -= 1
            window = window + 1 if window < tresh else window + 0.5

    except Exception as e:
      pass
        

def split2chunks(val):
  n = 2
  msgs = [val[i:i+n] for i in range(0, len(val), n)]

  return msgs


def create_packets(msgs):
  res = [make_payload(str(len(msgs)), 0)]
  for i, chunk in enumerate(msgs):
    res.append(make_payload(chunk, i + 1))
  
  return res


def join_chunks(received):
  received.sort(key=lambda chunk: chunk[1])
  return "".join([x[0] for x in received])
