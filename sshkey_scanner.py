import re
import subprocess

from lib import dict_update, valid_ipv4

class sshkey_scanner:
  def __init__(self, conf, pylanscan):
    self._conf = conf
    if "timeout" not in conf:
      self._conf["timeout"] = 5
    self._pylanscan = pylanscan
    self._read_hostkeys(conf["ssh_known_hosts"])

  def _read_hostkeys(self, path):
    keyfile = open(path, 'r')
    keys = keyfile.read().split("\\n")
    keys = map(lambda w: w.strip().split(), keys)
    keys = filter(lambda w: len(w) == 3, keys)
    keys = map(lambda w: {"hostname": w[0], "type": w[1], "key": w[2]}, keys)
    self._hostkeys = keys

  # makes hosts like [1.2.3.4]:5 to 1.2.3.4. Other formats remain unchanged
  def _xtrhost(self, hoststr):
    if re.match(r'^\[.+\]:\\d+$', hoststr):
      return re.split(r'\[|\]', hoststr)[1]
    else:
      return hoststr

  def scan(self):
    if not self._pylanscan._unknown_macs:
      return []

    scan_result = []
    keyscan_results = []
    for port in self._conf["scan_ports"]:
      cmd = ["ssh-keyscan", "-4", "-T", str(self._conf["timeout"]), "-p", str(port)]
      cmd += map(lambda w: w["ip"], self._pylanscan._unknown_macs)
      keyscan_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      if keyscan_result.returncode not in [0, 1]:
        die ("ssh-keyscan command fails, exit code: %i" % scan_result.returncode, exit_code = scan_result.returncode)
      keyscan_result = keyscan_result.stdout.decode("utf-8")
      keyscan_result = keyscan_result.split("\n")
      keyscan_result = filter(lambda w: w and w[0] != "#", keyscan_result)
      keyscan_result = map(lambda w: w.split(), keyscan_result)
      keyscan_result = map(lambda w: {"ip": self._xtrhost(w[0]), "type": w[1], "key": w[2]}, keyscan_result)
      keyscan_results += keyscan_result

    for found_key in keyscan_results:
      found_hostkey = filter(lambda w: w["type"] == found_key["type"] and w["key"] == found_key["key"], self._hostkeys)
      found_hostkey = list(found_hostkey)
      if not found_hostkey:
        continue
      else:
        found_hostkey = found_hostkey[0]
      # we have found a key in the hostkey table. Now we find its interface in the unknown_macs table
      unknown_macs_entry = filter(lambda w: found_key["ip"] == w["ip"], self._pylonscan._unknown_macs)
      unknown_macs_entry = list(unknown_macs_entry)
      if not unknown_macs_entry:
        die("should not happen")
      unknown_macs_entry = unknown_macs_entry[0]
      scan_result += {"ip": found_key["ip"], "iface": unknown_macs_entry["iface"], "hostname": found_hostkey["hostname"], "sshkey_type": found_hostkey["type"], "sshkey": found_hostkey["key"]}
    return scan_result

def create(conf, pylanscan):
  return sshkey_scanner(conf, pylanscan)
