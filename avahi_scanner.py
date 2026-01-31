import re
import subprocess

from lib import die, dict_update

class avahi_scanner:
  def __init__(self, conf, pylanscan):
    self._conf = conf
    self._pylanscan = pylanscan

  def scan(self):
    scan_result = subprocess.run(["avahi-browse", self._conf["avahi_browse_flags"]], stdout=subprocess.PIPE)
    if scan_result.returncode not in [0, 1]:
      die ("avahi-browse command fails, exit code: %i" % scan_result.returncode, exit_code = scan_result.returncode)

    scan_result = scan_result.stdout.decode("utf-8")
    scan_result = filter(lambda w: w.startswith("="), scan_result.split("\n"))
    scan_result = map(lambda w: w.split(";"), scan_result)
    scan_result = map(lambda w:{"iface": w[1], "fqdn": w[6], "ip": w[7]}, scan_result)
    scan_result = map(lambda w: dict_update(w, {"hostname": re.sub(r'[-\.].*$', '', w["fqdn"]) }), scan_result)
    return list(scan_result)

def create(conf, pylanscan):
  return avahi_scanner(conf, pylanscan)
