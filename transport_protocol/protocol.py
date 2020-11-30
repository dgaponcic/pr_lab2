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
    
    if is_valid(raw_payload) and random.random() > 0.7:
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

  for data in data2send:
    sender.sendto(data, receiver)
    payload, recv_addres = sender.recvfrom(1024, )

    while b"NACK" in payload:
      index = get_nack_index(payload)
      sender.sendto(data2send[index], receiver)
      payload, recv_addres = sender.recvfrom(1024)
        

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
  return "".join([x[0] for x in received])
