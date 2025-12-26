import subprocess

from lib import ip2rev, dict_update

class ddns_store():
  def __init__(self, conf):
    self._conf = conf
    self._nsu = dict()

  def get_record(self, rec_name, rec_type):
    result = subprocess.run(["host", "-v", "-T", "-4", "-p", str(self._conf["srv_port"]), "-t",
                                rec_type, rec_name, self._conf["srv_host"]],
                            stdout=subprocess.PIPE)
    if result.returncode not in [0, 1]:
      die ("host command fails, exit code: %i" % result.returncode, exit_code = result.returncode)
    result = result.stdout.decode("utf-8").split("\n")
    result = map(lambda w: w.split(), result)
    for i in result:
      # print ("i: " + i.__repr__())
      if len(i) >= 5 and i[0] == rec_name + "." and i[3] == rec_type:
        return i[4]
    return False

  def add_record(self, zone, rec_name, rec_type, rec_value):
    # print ("add_record(%s, %s, %s, %s)" % (zone, rec_name, rec_type, rec_value))
    cur_val = self.get_record(rec_name, rec_type)
    if cur_val == rec_value:
      return
    if not zone in self._nsu:
      self._nsu[zone] = []
    if cur_val:
      self._nsu[zone].append("update delete %s. %i IN %s %s" % (rec_name, ddns_default_refresh, rec_type, rec_value))
    self._nsu[zone].append("update add %s. %i IN %s %s" % (rec_name, ddns_default_refresh, rec_type, rec_value))
    if rec_type != "TXT":
      self.add_record(zone, rec_name, "TXT", ts)

  def store(self, output):
    hosts_found = set()
    output = map(lambda w: dict_update(w, {"dyn_fqdn": ".".join([w["hostname"], self._conf["fwd_zone"]]) }), output)
    for entry in output:
      dyn_fqdn = entry["dyn_fqdn"]
      iface_dyn_fqdn = ".".join([entry["iface"], entry["dyn_fqdn"]])
      ip = entry["ip"]
      revip_str = ip2rev(ip)
      self.add_record(self._conf["fwd_zone"], iface_dyn_fqdn, "A", ip)
      self.add_record(self._conf["rev_zone"], revip_str, "PTR", iface_dyn_fqdn + ".")
      if dyn_fqdn not in hosts_found:
        self.add_record(self._conf["fwd_zone"], dyn_fqdn, "A", ip)
        hosts_found.add(dyn_fqdn)

    print (self._nsu)
    for zone in self._nsu:
      nsu_input = ["server %s %i" % (self._conf["srv_host"], self._conf["srv_port"])]
      nsu_input += ["check-names no"]
      nsu_input += ["zone %s" % zone]
      nsu_input += self._nsu[zone]
      nsu_input += ["show", "send"]
      nsu_input += ["quit"]
      nsu_input = "\n".join(nsu_input)
      print (nsu_input)
      result = subprocess.run(["nsupdate", "-4", "-v", "-k", self._conf["key_path"]],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=nsu_input.encode())
      print ("nsupdate stdout:\n" + result.stdout.decode("utf-8") + "\nstderr:\n" + result.stderr.decode("utf-8"))
      if result.returncode not in [0, 1]:
        die ("host command fails, exit code: %i" % result.returncode, exit_code = result.returncode)

def create(conf):
  return ddns_store(conf)
