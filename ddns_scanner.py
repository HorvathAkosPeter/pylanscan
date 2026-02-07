class ddns_scanner:
  def __init__(self, conf, pylanscan):
    self._conf = conf
    self._pylanscan = pylanscan

  def scan(self):
    return []

def create(conf, pylanscan):
  return ddns_scanner(conf, pylanscan)
