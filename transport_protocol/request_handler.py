import hashlib

def is_valid(payload):
  data, control_hash = payload.decode("utf-8").split("|")
  return control_hash == hashlib.md5(data.encode("utf-8")).hexdigest()

def make_payload(val):
  control_hash = hashlib.md5(val.encode("utf-8")).hexdigest()
  return f'{val}|{control_hash}'.encode("utf-8")

def get_payload(raw_payload):
  return raw_payload.decode("utf-8").split("|")[0]
  