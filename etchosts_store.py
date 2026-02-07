etchosts_markup_config = {
  "start_line": "# pylanscan section start",
  "end_line": "# pylanscan section end",
  "record_markup": "%(ip)s %(hostname)s",
}

import markup_store from markup_store

class etchosts_store(markup_store):
  def __init__(self, conf, pylanscan):
    super.__init__(self, conf, pylanscan, etchosts_markup_config)

def create(conf, pylanscan):
  return etchosts_store(conf, pylanscan)
