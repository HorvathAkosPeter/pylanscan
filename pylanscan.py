#!/usr/bin/python3
import sys

from lib import ts_now, dict_update, uniq_functor, entry_compare

import config

class pylanscan():
  def __init__(self, config):
    self._ts = ts_now()
    self.scan_result = []

  def scan(self):
    for scanner_conf in config.scanners:
      scanner_lib = scanner_conf["scanner_type"]
      scanner = scanner_lib.create(scanner_conf, self)
      scan_result = scanner.scan()
      scan_result = map(lambda w: dict_update(w, {"scanner": scanner_lib.__name__}), scan_result)
      self.scan_result += scan_result

  def process(self):
    self.scan_result = filter(lambda w: w["iface"] in config.iface_prio_order, self.scan_result)
    self.scan_result = map(lambda w: dict_update(w, {"iface_prio": config.iface_prio_order.index(w["iface"])}), self.scan_result)
    self.scan_result = sorted(self.scan_result, key = lambda w: ",".join([str(w["iface_prio"]), w["ip"], w["hostname"]]) )
    self.scan_result = filter(uniq_functor(entry_compare), self.scan_result)
    #[print (i) for i in self.scan_result]
    #sys.exit(0)

  def store(self):
    for store_conf in config.stores:
      store_lib = store_conf["store_type"]
      store = store_lib.create(store_conf, self)
      store.store(self.scan_result)

main = pylanscan(config)
main.scan()
main.process()
main.store()
