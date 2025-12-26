class mac_scanner:
  def __init__(conf):
    self._conf = conf

  def scan():
    output = subprocess.run(["ip", "neigh", "ls"], stdout=subprocess.PIPE)
    if output.returncode != 0:
      die ("ip neigh ls command fails, exit code: %i" % output.returncode, exit_code = output.returncode)
    output = output.stdout.decode("utf-8")
    output = map(lambda w: w.split(), output)
    output = map(lambda w:{"iface": w[2], "mac": w[4], "ip": w[0]}, output)
    output = filter(lambda w: w["mac"] in self._conf["macs"], output)
    output = filter(lambda w: w["iface"] in iface_prio_order, output)
    output = map(lambda w: dict_update(w, {"iface_prio": iface_prio_order.index(w["iface"])}), output)
    output = map(lambda w: dict_update(w, {"hostname": self._conf["macs"][w[mac]] }), output)
    return output

def create(conf):
  return mac_scanner(conf)
