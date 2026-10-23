#!/bin/bash
# Inicializacao do servidor Comunicacao_Linux:
# garante a rota padrao pela WAN (eth0), gera chaves SSH, sobe cron/rsyslog
# e mantem o sshd em primeiro plano.
set -e

# Com duas redes, a saida para a Internet deve ser sempre pela WAN
if [ -n "$WAN_GATEWAY" ]; then
    ip route replace default via "$WAN_GATEWAY" dev eth0 2>/dev/null || true
fi

[ -f /etc/ssh/ssh_host_ed25519_key ] || ssh-keygen -A
mkdir -p /run/sshd

service rsyslog start >/dev/null 2>&1 || true
service cron start >/dev/null 2>&1 || true

exec /usr/sbin/sshd -D -e
