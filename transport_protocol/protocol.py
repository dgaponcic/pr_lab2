from transport_protocol.request_handler import is_valid, make_payload, get_packet, get_packet_index
from transport_protocol.socket_wrapper import SocketWrapper
import socket
import random
import uuid 
import errno
from contextlib import suppress

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
    new_conn.sendto(b'OK', sender)

    return SocketWrapper(new_conn, sender)

def get_stream_id(receiver):
  while True:
    with suppress(BlockingIOError):
      payload, addrs = receiver.recvfrom(1024)
      packet = get_packet(payload)

      if is_valid(payload) and packet["type"] == "INIT":
        stream_id = packet["data"]
        receiver.sendto(make_payload(stream_id, "INIT", "ACK", 0), addrs)
        return stream_id

def get_stream_length(stream_id, receiver):
    while True:
      with suppress(BlockingIOError):
        payload, addrs = receiver.recvfrom(1024)
        packet = get_packet(payload)
        if is_valid(payload) and packet["type"] == "LENGTH":
          receiver.sendto(make_payload(stream_id, "LENGTH", "ACK", 0), addrs)
          return int(packet["data"])

def read(receiver):
  received = []
  max_index = -1
  stream_id = get_stream_id(receiver)
  total_len = get_stream_length(stream_id, receiver)

  while len(received) != total_len:
    try:
      raw_payload, addr = receiver.recvfrom(1024)
      packet = get_packet(raw_payload)
      index = packet["index"]

      if packet["stream_id"] == stream_id and packet["type"] == "DATA" and is_valid(raw_payload) and random.random() > 0.3:
        receiver.sendto(make_payload(stream_id, "CONTROL", "ACK", index), addr)
        if index > max_index:
          max_index = index

        if not is_index_in_chunks(received, index):
          received.append((packet["data"], index))
      else:
        receiver.sendto(make_payload(stream_id, "CONTROL", "NACK", index), addr)
    except:
      for i in range(max_index + 1):
        if not is_index_in_chunks(received, i):
          receiver.sendto(make_payload(stream_id, "CONTROL", "NACK", i), addr)

  return join_chunks(received)

def init_write(stream_id, sender, receiver):
  sender.sendto(make_payload(stream_id, "INIT", stream_id, 0), receiver)
  while True:
    try:
      resp, addr = sender.recvfrom(1024)
      packet = get_packet(resp)
      if packet["type"] == "INIT" and packet["data"] == "ACK":
        break
    except:
      sender.sendto(make_payload(stream_id, "INIT", stream_id, 0), receiver)
      continue

def init_stream_len(stream_id, length, sender, receiver):
  sender.sendto(make_payload(stream_id, "LENGTH", str(length), 0), receiver)

  while True:
    try:
      resp, addr = sender.recvfrom(1024)
      packet = get_packet(resp)
      if packet["type"] == "LENGTH" and packet["data"] == "ACK":
        break
    except:
      sender.sendto(make_payload(stream_id, "LENGTH", str(len(data2send)), 0), receiver)
      continue


def write(val, sender):
  stream_id = str(uuid.uuid4())
  receiver = sender.connection
  msgs = split2chunks(val)
  data2send = create_packets(msgs, stream_id)
  window = 1
  pointer = 0
  waiting = set()
  ssthresh = 6

  init_write(stream_id, sender, receiver)
  init_stream_len(stream_id, len(data2send), sender, receiver)

  while pointer < len(data2send) or len(waiting) != 0:
    while len(waiting) < window and pointer < len(data2send):
      if pointer != 3 and pointer != 5 and pointer != 15:
        sender.sendto(data2send[pointer], receiver)
      waiting.add(pointer)
      pointer += 1

    with suppress(BlockingIOError):
      while True:
          payload, addr = sender.recvfrom(1024, socket.MSG_DONTWAIT)
          packet = get_packet(payload)

          if packet["type"] == "CONTROL" and packet["data"] == "NACK":
            index = packet["index"]
            sender.sendto(data2send[index], receiver)
            window *= 2 / 3

          elif packet["type"] == "CONTROL" and packet["data"] == "ACK":
            index = packet["index"]
            if index in waiting:
              waiting.remove(index)
            window = window + 1 if window < ssthresh else window + 0.5


def is_index_in_chunks(chunks, index):
  return any(index in chunk for chunk in chunks)


def split2chunks(val):
  n = 2
  msgs = [val[i:i+n] for i in range(0, len(val), n)]

  return msgs


def create_packets(msgs, stream_id):
  res = []
  for i, chunk in enumerate(msgs):
    res.append(make_payload(stream_id, "DATA", chunk, i))
  
  return res


def join_chunks(received):
  received.sort(key=lambda chunk: chunk[1])
  return "".join([x[0] for x in received])
