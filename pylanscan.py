#!/usr/bin/python3
import sys

from lib import ts_now, dict_update, uniq_functor, entry_compare

import config

ts = ts_now()
output = []

for i in config.scanners:
  scanner_lib = i["scanner_type"]
  scanner = scanner_lib.create(i)
  scan_result = scanner.scan()
  output += scan_result

output = filter(lambda w: w["iface"] in config.iface_prio_order, output)
output = map(lambda w: dict_update(w, {"iface_prio": config.iface_prio_order.index(w["iface"])}), output)
output = sorted(output, key = lambda w: ",".join([str(w["iface_prio"]), w["ip"], w["hostname"]]) )
output = filter(uniq_functor(entry_compare), output)

#[print (i) for i in output]
#sys.exit(0)

for i in config.stores:
  store_lib = i["store_type"]
  store = store_lib.create(i)
  store.store(output)
