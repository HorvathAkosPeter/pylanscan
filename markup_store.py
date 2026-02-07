import os
import pathlib
import subprocess

from lib import search_list, die

class markup_store():
  def __init__(self, conf, pylanscan, markup_config):
    self._conf = conf
    self._pylanscan = pylanscan
    self._markup_config = markup_config

  def read_file(self):
    try:
      with open(self._conf["path"]) as file:
        content = file.read()
    except FileNotFoundError:
      return ([], [], [])

    content = content.split("\n")

    begin = search_list(content, self._markup_config["start_line"])
    if begin is False:
      end = False
    else:
      end = search_list(content, self._markup_config["end_line"], after=begin)

    if begin is False and end is False:
      return (content, [], [])
    elif begin is True and end is False:
      return (content[:begin], content[begin+1:], [])
    elif begin is True and end is True:
      return (content[:begin], content[begin+1:end], content[end+1:])
    else:
      die ("unreachable")

  def make_lines(self, scan_result):
    return [self._markup_config["record_markup"] % entry for entry in scan_result]
    
  def write_file(self, before, lines, after):
    new_all_lines = before + [self._markup_config["start_line"]] + lines + [self._markup_config["end_line"]] + after
    new_content = "\n".join(new_all_lines)
    bkp_path = self._conf["path"] + "~" + self._pylanscan._ts
    if pathlib.Path(self._conf["path"]).is_file():
      bkp_result = subprocess.run(["cp", "-vfa", self._conf["path"], bkp_path])
      if bkp_result.returncode != 0:
        die ("can not create backup file %s" % bkp_path)
    with open(self._conf["path"], "w") as file:
      file.write(new_content)

  def store(self, scan_result):
    (before, lines, after) = self.read_file()
    new_lines = self.make_lines(scan_result)
    if "\n".join(lines) != "\n".join(new_lines):
      self.write_file(before, new_lines, after)
