#!/bin/bash

current_dir=$(pwd)

# trap ctrl-c and call ctrl_c()
function ctrl_c() {
  P_ID="$(ps e -ww -A | grep "_TAG=ofagent-tcpdump" | grep -v grep | awk '{print $1}')"
  if [ -n "$P_ID" ]; then
    kill -9 $P_ID
  fi

  OF_AGENT=$(kubectl get pods -l app=ofagent -o name)
  kubectl cp $OF_AGENT:out.pcap $current_dir/ofagent.pcap
  exit 0
}
trap ctrl_c SIGINT

OF_AGENT=$(kubectl get pods -l app=ofagent -o name)
#kubectl exec $OF_AGENT -- apk update
#kubectl exec $OF_AGENT -- apk add tcpdump
kubectl exec $OF_AGENT -- apt update
kubectl exec $OF_AGENT -- apt install tcpdump -y
#kubectl exec $OF_AGENT -- mv /usr/sbin/tcpdump /usr/bin/tcpdump
_TAG=ofagent-tcpdump kubectl exec $OF_AGENT -- tcpdump -nei eth0 -w out.pcap&

echo -e "Capturing OfAgent tcpdump:\n"
while true; do
    echo -ne "."
    sleep 1
done

