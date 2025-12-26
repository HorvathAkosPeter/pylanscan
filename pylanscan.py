#!/usr/bin/python3
from lib import *

import config

import scanner_avahi
import scanner_ddns
import store_ddns

import datetime
import ipaddress
import re
import subprocess
import sys

nsu = dict()
ts = ts_now()

output = sorted(output, key = lambda w: ",".join([str(w["iface_prio"]), w["fqdn"]]) )
output = filter(uniq_functor(entry_compare), output)

#[print (i) for i in output]
#sys.exit(0)

output = []

hosts_found = set()

