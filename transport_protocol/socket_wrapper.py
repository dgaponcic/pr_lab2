import socket, struct
import math


def _seconds_to_sockopt_format(seconds):
  microseconds_per_second = 1000000
  whole_seconds = int(math.floor(seconds))
  whole_microseconds = int(math.floor((seconds % 1) * microseconds_per_second))
  return struct.pack("ll", whole_seconds, whole_microseconds)

class SocketWrapper(object):
  def __init__(self, sock, connection):
    self.sock = sock
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, _seconds_to_sockopt_format(0.1))
    self.connection = connection
  

  def fileno(self):
    return self.sock.fileno()


  def recvfrom(self, buffer, *args):
    if args:
      return self.sock.recvfrom(buffer, args[0])
    else:
      return self.sock.recvfrom(buffer)


  def sendto(self, msg, addr):
    self.sock.sendto(msg, addr)
