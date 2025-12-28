import re
import subprocess
import sys

from lib import dict_update, valid_ipv4

class localif_scanner:
  def __init__(self, conf, pylanscan):
    self._conf = conf
    self._pylanscan = pylanscan
    self._hostname = self._pylanscan._hostname

  def scan(self):
    scan_result = subprocess.run(["ip", "addr", "ls"], stdout=subprocess.PIPE)
    if scan_result.returncode != 0:
      die ("ip addr ls command fails, exit code: %i" % scan_result.returncode, exit_code = scan_result.returncode)
    scan_result = scan_result.stdout.decode("utf-8")
    scan_result = scan_result.split("\n")
    scan_result = map(lambda w: w.split(), scan_result)
    found_ips = []
    cur_if = None
    for line in scan_result:
      if len(line) < 2:
        continue
      # print (line)
      if re.match("^\\d+:", line[0]):
        cur_if = re.sub(r':', '', line[1])
      if line[0] == "inet":
        cur_ip = re.sub(r'/.*$', '', line[1])
        found_ips.append({"hostname": self._pylanscan._hostname, "iface": cur_if, "ip": cur_ip})
    # print ("found_ips: ")
    # print (found_ips)
    # sys.exit(0)
    return found_ips

def create(conf, pylanscan):
  return localif_scanner(conf, pylanscan)
