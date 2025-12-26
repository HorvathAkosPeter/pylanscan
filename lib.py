def die(msg, exit_code=-1):
  print (msg, file=sys.stderr)
  sys.exit(exit_code)

def dict_update(the_dict, update_dict):
  ret = dict(the_dict)
  ret.update(update_dict)
  return ret

class uniq_functor(object):
  def __init__(self, _compare):
    self._compare = _compare
    self._last = None
  def __call__(self, x):
    if self._last == None:
      self._last = x
      return True
    else:
      iseq = self._compare(self._last, x)
      self._last = x
      return not iseq

def entry_compare(e1, e2):
  return e1.__repr__() == e2.__repr__()

def ts_now():
  now = datetime.datetime.now(tz=datetime.timezone.utc)
  return now.strftime("%Y%m%d%H%M%S%f")

def ip2rev(ip):
  return ".".join(ip.split(".")[::-1])+".in-addr.arpa"
