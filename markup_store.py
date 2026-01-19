markup_config = {
  "start_line": "# pylanscan section start",
  "end_line": "# pylanscan section end",
  "record_markup": "%(ip)s %(hostname)s",
  "inverse_markup": r'?^P<ip>[^ ]+ ?P<hostname>$'
}

class markup_store():
  def __init__(self, conf, pylanscan, markup_config):
    self._conf = conf
    self._pylanscan = pylanscan
    self._markup_config = markup_config

  def store(self, scan_result):
    current_hosts = self.get_current_hosts()
    scanned_hosts = self.make_scanned_hosts()
    self.
    scanned_hosts = {}
    for i in scan_result:
      scanned_hosts[i["hostname"]]=i["ip"]
    
