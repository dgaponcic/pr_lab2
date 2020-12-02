import hashlib

def is_valid(payload):
  packet = payload.decode("utf-8").split("|")
  data = packet[2]
  control_hash = packet[3]
  
  return control_hash == hashlib.md5(data.encode("utf-8")).hexdigest()


def get_packet(raw_payload):
  stream_id, packet_type, data, _, index = raw_payload.decode("utf-8").split("|")

  return {
    "stream_id": stream_id, 
    "type": packet_type, 
    "data": data, 
    "index": int(index)
  }


def make_payload(stream_id, packet_type, val, index):
  control_hash = hashlib.md5(val.encode("utf-8")).hexdigest()
  return f'{stream_id}|{packet_type}|{val}|{control_hash}|{index}'.encode("utf-8")


def get_packet_index(payload):
  return int(payload.decode("utf-8").split("|")[-1])
