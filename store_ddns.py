def get_record(rec_name, rec_type):
  result = subprocess.run(["host", "-v", "-T", "-4", "-p", str(ddns_srv_port), "-t", rec_type, rec_name, ddns_srv_host],
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

def add_record(zone, rec_name, rec_type, rec_value):
  # print ("add_record(%s, %s, %s, %s)" % (zone, rec_name, rec_type, rec_value))
  cur_val = get_record(rec_name, rec_type)
  if cur_val == rec_value:
    return
  if not zone in nsu:
    nsu[zone] = []
  if cur_val:
    nsu[zone].append("update delete %s. %i IN %s %s" % (rec_name, ddns_default_refresh, rec_type, rec_value))
  nsu[zone].append("update add %s. %i IN %s %s" % (rec_name, ddns_default_refresh, rec_type, rec_value))
  if rec_type != "TXT":
    add_record(zone, rec_name, "TXT", ts)

for entry in output:
  dyn_fqdn = entry["dyn_fqdn"]
  iface_dyn_fqdn = ".".join([entry["iface"], entry["dyn_fqdn"]])
  ip = entry["ip"]
  revip_str = ip2rev(ip)
  add_record(ddns_fwd_zone, iface_dyn_fqdn, "A", ip)
  add_record(ddns_rev_zone, revip_str, "PTR", iface_dyn_fqdn + ".")
  if dyn_fqdn not in hosts_found:
    add_record(ddns_fwd_zone, dyn_fqdn, "A", ip)
    hosts_found.add(dyn_fqdn)

print (nsu)
for zone in nsu:
  nsu_input = ["server %s %i" % (ddns_srv_host, ddns_srv_port)]
  nsu_input += ["check-names no"]
  nsu_input += ["zone %s" % zone]
  nsu_input += nsu[zone]
  nsu_input += ["show", "send"]
  nsu_input += ["quit"]
  nsu_input = "\n".join(nsu_input)
  print (nsu_input)
  result = subprocess.run(["nsupdate", "-4", "-v", "-k", ddns_key_path],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=nsu_input.encode())
  print ("nsupdate stdout:\n" + result.stdout.decode("utf-8") + "\nstderr:\n" + result.stderr.decode("utf-8"))
  if result.returncode not in [0, 1]:
    die ("host command fails, exit code: %i" % result.returncode, exit_code = result.returncode)
