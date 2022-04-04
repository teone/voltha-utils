"""
This program takes as input a file generated from the voltha logs with:
cat Test.log | grep openolt | grep update_flows_incrementally | awk '{for (i=2;i<=NF;i++){printf $i; if (i < NF) {printf FS};}printf RS}' | jq -r '(.ts + " | " + .msg + " | " + .flows)' > openolt.flows.log
"""
import re

input_file = "/home/teone/Sites/voltha/voltha-logs/periodic-voltha-test-bbsim/1006/openolt.flows.log"
nni_port = "1048576"

file1 = open(input_file, 'r')
Lines = file1.readlines()

for line in Lines:
    line = line.strip()
    if len(line) == 0 or line.startswith("#"):
        continue

    time = line.split("|")[0]
    flowInfo = line.split("|")[-1]

    flowToAdd = re.search(r'to_add:<(.+)> to_remove:<>', flowInfo) is not None

    outPrefix = ""
    if flowToAdd:
        outPrefix = "Adding "
    else:
        outPrefix = "Removing "

    lldp = re.search(r'.*eth_type:35020.*', flowInfo)
    if lldp:
        print("{} - {} LLDP on NNI".format(time, outPrefix))
        continue

    nni_dhcp = re.search(r'.*port:{}.*eth_type:2048.*'.format(nni_port), flowInfo)
    if nni_dhcp:
        print("{} - {} DHCP on NNI".format(time, outPrefix))
        continue

    eapol = re.search(r'.*eth_type:34958.*vlan_vid:([0-9]+).*tunnel_id:([0-9]+).*meter_id:([0-9]+).*', flowInfo)
    if eapol:
        vlan = int(eapol.group(1)) - 4096
        in_port = eapol.group(2)
        meter_id = eapol.group(3)
        print("{} - {} EAPOL with VLAN {} on {} with meter {}".format(time, outPrefix, vlan, in_port, meter_id))
        continue

    dhcp = re.search(r'.*vlan_vid:([0-9]+).*ip_proto:17.*tunnel_id:([0-9]+).*meter_id:([0-9]+).*', flowInfo)
    if dhcp:
        vlan = int(dhcp.group(1)) - 4096
        in_port = dhcp.group(2)
        meter_id = dhcp.group(3)
        print("{} - {} DHCP with VLAN {} on {} with meter {}".format(time, outPrefix, vlan, in_port, meter_id))
        continue

    print("\tDataplane flow: {}",format(line))