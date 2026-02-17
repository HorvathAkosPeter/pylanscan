* config: yaml-based configuration
* config: more complex structure: a local termux ddns on the phone/router, as first-level store, then merge it into a hosted net bind
* ddns_scan: scan plugin as the AXFR query of a friendly DNS server (like bind in a termux)
* ddns_store: should re-use the result of a previous ddns_scan
* ddns_store: using some type of DNSSEC in the ddns store
* lib: debug output to understand, which can found what
* mac_scanner: config should use mac-host pair list from an external path
* nmap_scanner: utilize nmap ping or tcp scan to discover hosts
* pylanscan: if there are contradicting results, report or alarm
* pylanscan: some scan results can have multiple or overlapping entries, some not. Handle both.
* pylanscan: we might have some reporting or alarming for unknown macs/ips found
* pylanscan: we would need some dependency handling - sshkey_scanner can only run after mac_scanner has already created a list of the unknown macs
* sshkey_scanner: could also have a key list. Currently it can only use a host key format (as in /etc/ssh/ssh_known_hosts)
* sshkey_scanner: ssh-keygen has a subnet scanning feature and seems working quite well
* tlscert_scanner: identification based on tls certificates

# DONE #
* ddns_store: bind9 does not want to give AXFR queries for ANY record type. (Fun: -t AXFR but without "-l" works)
    (workaround: host -t AXFR (without "-l") does exactly what we wanted)
* ddns_store: axfr scan as source
* envfile_store: environment variable files as store, like ~/.environ
* etchosts_store: /etc/hosts as store
* etchosts_store: fqdn support
* etchosts_store: backup ends with tilde
