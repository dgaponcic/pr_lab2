import hashlib

def is_valid(payload):
  data, control_hash, index = payload.decode("utf-8").split("|")

  return control_hash == hashlib.md5(data.encode("utf-8")).hexdigest()


def get_payload(raw_payload):
  chunk = raw_payload.decode("utf-8").split("|")
  data = chunk[0]
  index = int(chunk[-1])

  return data, index


def make_payload(val, index):
  control_hash = hashlib.md5(val.encode("utf-8")).hexdigest()
  return f'{val}|{control_hash}|{index}'.encode("utf-8")


def get_nack_index(payload):
  return int(payload.decode("utf-8").split("|")[1])
