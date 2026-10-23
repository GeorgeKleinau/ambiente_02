#!/bin/bash
# Inicializacao do Cliente_Linux:
# 1) firewall: o cliente fala apenas com a LAN (sem Internet)
# 2) sobe o supervisord: VNC (Xtigervnc) + XFCE + noVNC (porta 6080)
set -e

if [ -n "$LAN_SUBNET" ]; then
    iptables -F OUTPUT
    iptables -A OUTPUT -o lo -j ACCEPT
    iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    iptables -A OUTPUT -d "$LAN_SUBNET" -j ACCEPT
    iptables -A OUTPUT -j REJECT
fi

rm -f /tmp/.X1-lock /tmp/.X11-unix/X1
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
