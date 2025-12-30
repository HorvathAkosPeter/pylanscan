* sshkey_scanner could also have a key list. Currently it can only use a host key format (as in /etc/ssh/ssh_known_hosts)
* we would need some dependency handing - sshkey_scanner can only run after mac_scanner has already created a list of the unknown macs
* we might have some reporting or alarming for unknown macs/ips found
* debug output to understand, which can found what
* if there are contradicting results, report or alarm
* yaml-based configuration
