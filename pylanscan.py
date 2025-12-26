#!/usr/bin/python3
from lib import *

import config

import importlib

#import avahi_scanner
#import mac_scanner
#import ddns_store

import datetime
import ipaddress
import re
import subprocess
import sys

nsu = dict()
ts = ts_now()
output = []

for i in config.scanners:
  scanner_lib = importlib(i["scanner_type"])
  scanner = scanner_lib.create(i)
  scan_result = scanner.scan()
  output += scan_result

output = map(lambda w: dict_update(w, {"dyn_fqdn": ".".join([w["hostname"], ddns_fwd_zone]) }), output)
output = sorted(output, key = lambda w: ",".join([str(w["iface_prio"]), w["ip"], w["hostname"]]) )
output = filter(uniq_functor(entry_compare), output)

[print (i) for i in output]
sys.exit(0)

hosts_found = set()

for i in config.stores:
  store_lib = importlib(i["store_type"])
  store = store_lib.create(i)
  store.store(output)
