import copy

from markup_store import markup_store

etchosts_markup_config = {
  "start_line": "# pylanscan section start",
  "end_line": "# pylanscan section end",
  "record_markup": "%(ip)s %(hostname)s",
}

class etchosts_store(markup_store):
  def __init__(self, conf, pylanscan):
    cfg = copy.copy(etchosts_markup_config)
    if "domain" in conf:
      cfg["record_markup"] = cfg["record_markup"] + " %(hostname)s." + conf["domain"]
    super().__init__(conf, pylanscan, cfg)

def create(conf, pylanscan):
  return etchosts_store(conf, pylanscan)
