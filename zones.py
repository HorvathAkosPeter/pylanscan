#!/usr/bin/python3
import subprocess

import ddns_store
import config

from lib import die

ddns_cfg = []

for e in dir(config):
  i = getattr(config, e)
  try:
    if "store_type" in i and i["store_type"] == "ddns_store":
      ddns_cfg = i
      break
  except TypeError:
    pass

if not ddns_cfg:
  die ("no ddns_store in configured entities")

for zone in [ddns_cfg["fwd_zone"], ddns_cfg["rev_zone"]]:
  cmd = ["host", "-4", "-T", "-p", str(ddns_cfg["srv_port"]), "-v", "-t", "AXFR", zone + ".", ddns_cfg["srv_host"]]
  print (" ".join(cmd))
  subprocess.run(cmd)
