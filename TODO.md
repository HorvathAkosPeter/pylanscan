* sshkey_scanner could also have a key list. Currently it can only use a host key format (as in /etc/ssh/ssh_known_hosts)
* we would need some dependency handing - sshkey_scanner can only run after mac_scanner has already created a list of the unknown macs
* we might have some reporting or alarming for unknown macs/ips found
* debug output to understand, which can found what
* if there are contradicting results, report or alarm
* yaml-based configuration
* utilize nmap ping or tcp scan
* ssh-keygen has a subnet scanning feature and seems working quite well
* using some type of DNSSEC in the ddns store
* axfr scan as source
* /etc/hosts as store
* environment variables as store
* more complex structure: a local termux ddns on the phone/router, as first-level store, then merge it into a hosted net bind
* bind9 does not want to give AXFR queries for ANY record type. (Fun: -t AXFR but without "-l" works)
