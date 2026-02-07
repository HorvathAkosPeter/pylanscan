import copy

from markup_store import markup_store

envfile_markup_config = {
  "start_line": "# pylanscan section start",
  "end_line": "# pylanscan section end",
  "record_markup": "%(hostname)s=%(ip)s",
}

class envfile_store(markup_store):
  def __init__(self, conf, pylanscan):
    cfg = copy.copy(envfile_markup_config)
    if conf["exports"]:
      cfg["record_markup"] = "export " + cfg["record_markup"]
    super().__init__(conf, pylanscan, envfile_markup_config)

def create(conf, pylanscan):
  return envfile_store(conf, pylanscan)
