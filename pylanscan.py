#!/usr/bin/python3
import importlib
import os
import sys

from lib import ts_now, dict_update, uniq_functor, entry_compare, die, debug

import config

class pylanscan():
  def __init__(self, config):
    self._config = config
    self._ts = ts_now()
    self._unknown_macs = []
    self.scan_result = []
    if hasattr(config, "hostname"):
      self._hostname = config.hostname
    elif "HOSTNAME" in os.environ and os.environ["HOSTNAME"]:
      self._hostname = os.environ["HOSTNAME"]
    else:
      self._hostname = os.uname().nodename

  def add_unknown_macs(self, mac_list):
    self._unknown_macs += mac_list

  def scan(self):
    for scanner_conf in config.scanners:
      debug (3, "--- Scan " + scanner_conf["scanner_type"] + ":")
      scanner_lib = importlib.import_module(scanner_conf["scanner_type"])
      scanner = scanner_lib.create(scanner_conf, self)
      scan_result = scanner.scan()
      scan_result = map(lambda w: dict_update(w, {"scanner": scanner_lib.__name__}), scan_result)
      for i in scan_result:
        debug(3, dict(sorted(i.items())))
      self.scan_result += scan_result

  def process(self):
    self.scan_result = filter(lambda w: w["iface"] in config.iface_prio_order, self.scan_result)
    self.scan_result = map(lambda w: dict_update(w, {"iface_prio": config.iface_prio_order.index(w["iface"])}), self.scan_result)
    self.scan_result = sorted(self.scan_result, key = lambda w: ",".join([str(w["iface_prio"]), w["ip"], w["hostname"]]) )
    self.scan_result = filter(uniq_functor(entry_compare), self.scan_result)
    if config.verbose >= 3:
      debug (3, "--- Summarized result:")
      [debug (3, i) for i in self.scan_result]

  def store(self):
    for store_conf in config.stores:
      debug (3, "--- Store " + store_conf["store_type"] + ":")
      store_lib = importlib.import_module(store_conf["store_type"])
      store = store_lib.create(store_conf, self)
      store.store(self.scan_result)

main = pylanscan(config)
main.scan()
main.process()
main.store()
