import socket
import json
import random
import hashlib
# import select
# from threading import Thread
from transport_protocol.socket_wrapper import SocketWrapper
from transport_protocol.request_handler import is_valid, make_payload, get_payload

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
    print("created new connection")

    return SocketWrapper(new_conn, sender)


def read(receiver):
  while True:
    raw_payload, addr = receiver.recvfrom(1024)
    if is_valid(raw_payload) and random.random() > 0.7:
      receiver.sendto(b'ACK', addr)
      print("sending ack")
      return get_payload(raw_payload)
    else:
      receiver.sendto(b'NACK', addr)
      print("sending nack")


def write(val, sender):
  receiver = sender.connection
  sender.sendto(make_payload(val), receiver)
  payload, recv_addres = sender.recvfrom(1024)

  while b"NACK" in payload:
    sender.sendto(make_payload(val), receiver)
    payload, recv_addres = sender.recvfrom(1024)
