class avahi_scanner:
  def __init__(conf):
    self._conf = conf

  def scan():
    output = subprocess.run(["avahi-browse", avahi_browse_flags], stdout=subprocess.PIPE)
    if output.returncode not in [0, 1]:
      die ("avahi-browse command fails, exit code: %i" % output.returncode, exit_code = output.returncode)

    output = output.stdout.decode("utf-8")
    output = filter(lambda w: w.startswith("="), output.split("\n"))
    output = map(lambda w: w.split(";"), output)
    output = map(lambda w:{"iface": w[1], "fqdn": w[6], "ip": w[7]}, output)
    output = filter(lambda w: w["iface"] in iface_prio_order, output)
    output = map(lambda w: dict_update(w, {"iface_prio": iface_prio_order.index(w["iface"])}), output)
    output = map(lambda w: dict_update(w, {"hostname": re.sub(r'[-\.].*$', '', w["fqdn"]) }), output)
    return output

def create(conf):
  return avahi_scanner(conf)
