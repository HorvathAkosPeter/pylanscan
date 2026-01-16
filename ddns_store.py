import subprocess
import sys

from lib import ip2rev, dict_update, die

class ddns_store():
  def __init__(self, conf, pylanscan):
    self._conf = conf
    self._nsu = dict()
    self._pylanscan = pylanscan

  def get_record(self, rec_name, rec_type):
    host_result = subprocess.run(["host", "-v", "-T", "-4", "-p", str(self._conf["srv_port"]), "-t",
                                rec_type, rec_name, self._conf["srv_host"]],
                            stdout=subprocess.PIPE)
    if host_result.returncode not in [0, 1]:
      die ("host command fails, exit code: %i" % host_result.returncode, exit_code = host_result.returncode)
    host_result = host_result.stdout.decode("utf-8").split("\n")
    host_result = map(lambda w: w.split(), host_result)
    results = []
    for i in host_result:
      # print ("i: " + i.__repr__())
      if len(i) >= 5 and i[0] == rec_name + "." and i[3] == rec_type:
        results.append(i[4])
    # print (rec_name, rec_type, results)
    return results

  def add_record(self, zone, rec_name, rec_type, rec_value):
    print ("add_record(%s, %s, %s, %s)" % (zone, rec_name, rec_type, rec_value))
    cur_vals = self.get_record(rec_name, rec_type)
    need_to_add = True
    if not zone in self._nsu:
      self._nsu[zone] = []
    for cur_val in cur_vals:
      # print ("cur_val: %s, rec_value: %s" % (cur_val, rec_value))
      if cur_val == rec_value:
        need_to_add = False
      else:
        self._nsu[zone].append("update delete %s. %i IN %s %s" % (rec_name, self._conf["default_refresh"], rec_type, cur_val))
    if need_to_add:
      self._nsu[zone].append("update add %s. %i IN %s %s" % (rec_name, self._conf["default_refresh"], rec_type, rec_value))
    if rec_type != "TXT" and (need_to_add or len(self.get_record(rec_name, "TXT")) > 1):
      self.add_record(zone, rec_name, "TXT", "\"" + self._pylanscan._ts + "\"")

  def store(self, scan_result):
    hosts_found = set()
    scan_result = map(lambda w: dict_update(w, {"dyn_fqdn": ".".join([w["hostname"], self._conf["fwd_zone"]]) }), scan_result)
    for entry in scan_result:
      dyn_fqdn = entry["dyn_fqdn"]
      if entry["hostname"] == self._pylanscan._hostname:
        iface_dyn_fqdn = ".".join([entry["iface"], self._pylanscan._hostname, self._conf["fwd_zone"]])
      else:
        iface_dyn_fqdn = ".".join([entry["hostname"], entry["iface"], self._pylanscan._hostname, self._conf["fwd_zone"]])
      ip = entry["ip"]
      revip_str = ip2rev(ip)
      self.add_record(self._conf["fwd_zone"], iface_dyn_fqdn, "A", ip)
      if dyn_fqdn not in hosts_found:
        self.add_record(self._conf["fwd_zone"], dyn_fqdn, "A", ip)
        self.add_record(self._conf["rev_zone"], revip_str, "PTR", dyn_fqdn + ".")
        hosts_found.add(dyn_fqdn)
      else:
        self.add_record(self._conf["rev_zone"], revip_str, "PTR", iface_dyn_fqdn + ".")

    # print (self._nsu)
    for zone in self._nsu:
      if not self._nsu[zone]:
        continue
      nsu_input = ["server %s %i" % (self._conf["srv_host"], self._conf["srv_port"])]
      nsu_input += ["check-names no"]
      nsu_input += ["zone %s" % zone]
      nsu_input += self._nsu[zone]
      nsu_input += ["show", "send"]
      nsu_input += ["quit"]
      nsu_input = "\n".join(nsu_input)
      print (nsu_input)
      # sys.exit(0)
      result = subprocess.run(["nsupdate", "-4", "-v", "-k", self._conf["key_path"]],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=nsu_input.encode())
      print ("nsupdate stdout:\n" + result.stdout.decode("utf-8") + "\nstderr:\n" + result.stderr.decode("utf-8"))
      if result.returncode not in [0, 1]:
        die ("host command fails, exit code: %i" % result.returncode, exit_code = result.returncode)

def create(conf, pylanscan):
  return ddns_store(conf, pylanscan)
