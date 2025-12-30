import re
import subprocess

from lib import dict_update, valid_ipv4

class sshkey_scanner:
  def __init__(self, conf, pylanscan):
    self._conf = conf
    self._pylanscan = pylanscan

  def scan(self):
    scan_result = subprocess.run(["ip", "neigh", "ls"], stdout=subprocess.PIPE)
    if scan_result.returncode != 0:
      die ("ip neigh ls command fails, exit code: %i" % scan_result.returncode, exit_code = scan_result.returncode)
    scan_result = scan_result.stdout.decode("utf-8")
    scan_result = scan_result.split("\n")
    scan_result = map(lambda w: w.split(), scan_result)
    scan_result = filter(lambda w: len(w)>=5, scan_result)
    scan_result = map(lambda w:{"iface": w[2], "mac": w[4], "ip": w[0]}, scan_result)
    scan_result = filter(lambda w: valid_ipv4(w["ip"]), scan_result)
    unknown_macs = filter(lambda w: w["mac"] not in self._conf["macs"], scan_result)
    self._pylanscan.add_unknown_macs(unknown_macs)
    scan_result = filter(lambda w: w["mac"] in self._conf["macs"], scan_result)
    scan_result = map(lambda w: dict_update(w, {"hostname": self._conf["macs"][w["mac"]] }), scan_result)
    return scan_result

def create(conf, pylanscan):
  return mac_scanner(conf, pylanscan)
