import os

avahi_scan = {
  "scanner_type": "avahi_scanner",
  "avahi_browse_flags": "-arpt" if "TERMUX_VERSION" in os.environ else "-arkpt"
}

mac_scan = {
  "scanner_type": "mac_scanner",
  "macs": {
    "0a:d9:da:78:e9:3d": "derpeter",
    "a6:c0:37:bf:d4:3e": "derpeter",
    "14:5f:94:de:84:5c": "diekati",
    "24:c6:13:0f:50:dd": "diekati2",
    # "1e:6c:d1:37:18:49": "e7_1", # randomizes
    "b0:5a:da:23:5b:40": "hpoj",
    "80:c1:6e:44:ca:32": "hpmaxx",
    "7c:e9:d3:82:3c:53": "hpmaxx",
    "f8:5e:a0:06:fc:02": "katilaptop2",
    "f0:c4:2f:08:61:a8": "matepad1",
    "90:65:84:4b:ca:da": "ppyur",
    "52:54:00:35:c9:33": "ppyur",
    "52:54:00:c5:6e:82": "ppyur_win",
    "ce:0f:3a:da:f6:e4": "sony",
    "46:b3:02:66:fe:01": "tcl"
  }
}

localif_scan = {
  "scanner_type": "localif_scanner"
}

sshkey_scan = {
  "scanner_type": "sshkey_scanner",
  "ssh_known_hosts": (os.environ["TERMUX__PREFIX"] if "TERMUX__PREFIX" in os.environ else "") + "/etc/ssh/ssh_known_hosts",
  "scan_ports": [22, 2222, 8022],
  "timeout": 5
}

#tlscert_scan = {
#  "scanner_type": tlscert_scan,
#}

ddns_stor = {
  "store_type": "ddns_store",
  "srv_host": "127.0.0.1",
  "srv_port": 9053,
  "key_path": (os.environ["TERMUX__PREFIX"] if "TERMUX__PREFIX" in os.environ else "") + "/etc/bind/ddns.key.conf",
  "fwd_zone": "dyn.hwen.de",
  "rev_zone": "168.192.in-addr.arpa",
  "rev_mask": "192.168.0.0/16",
  "default_refresh": 3600
}

etchosts_stor = {
  "store_type": "etchosts_store",
  "path": (os.environ["TERMUX__PREFIX"] if "TERMUX__PREFIX" in os.environ else "") + "/etc/hosts"
}

envsh_stor = {
  "store_type": "envsh_store",
  "path": os.environ["HOME"] + "/.environment"
}

iface_prio_order = [ "ap0", "wlan1", "wlan0", "virbr0" ]

if os.uname().nodename == "cp050w60457":
  hostname = "ppyur"

# tlscert_scanner is not ready yet!
scanners = [ localif_scan, mac_scan, avahi_scan, sshkey_scan ]
# scanners = [ mac_scan, sshkey_scan ]
stores = [ ddns_stor ]
# stores = [ ddns_stor, etchosts_stor, envsh_stor ]
# stores = [ ddns_stor, etc_hosts, env_file ]
# hosts store, environment store, dns zone scan
# hostname =  "well"
verbose = 4
