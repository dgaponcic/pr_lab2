class PhoneLookup:
  def __init__(self):
    self.register = {"0010": {"host": "127.0.0.1", "port": 10001}}

  def get_addr(self, number):
    return self.register[number]
