# ------------------------------------------------------------------
# Projeto ambiente_02 - SERVIDOR Base_Linux (Debian 13 "trixie")
# Terminal/CLI + SSH, pronto para instalar servicos (web, ftp, samba...)
# ------------------------------------------------------------------
FROM debian:13

LABEL projeto="ambiente_02" \
      papel="servidor" \
      descricao="Debian 13 completo para treino de Linux (CLI + SSH)"

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Sao_Paulo \
    LANG=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8

RUN apt-get update && apt-get -y full-upgrade && \
    apt-get install -y --no-install-recommends \
        openssh-server sudo ca-certificates locales tzdata \
        apt-utils apt-transport-https gnupg lsb-release \
        bash-completion man-db manpages less \
        vim nano curl wget git unzip zip tar xz-utils rsync \
        procps psmisc htop lsof file tree \
        iproute2 iputils-ping net-tools dnsutils traceroute \
        tcpdump netcat-openbsd nmap ethtool iptables \
        cron logrotate rsyslog && \
    sed -i 's/^# *pt_BR.UTF-8/pt_BR.UTF-8/' /etc/locale.gen && locale-gen && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Usuarios: admin (sudo) e root. SSH com senha, root sem login por SSH.
ARG ADMIN_SENHA=adm123
ARG ROOT_SENHA=root123
RUN useradd -m -s /bin/bash -G sudo admin && \
    echo "admin:${ADMIN_SENHA}" | chpasswd && \
    echo "root:${ROOT_SENHA}" | chpasswd && \
    mkdir -p /run/sshd && \
    sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    rm -f /etc/ssh/ssh_host_*

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY motd /etc/motd
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 22
WORKDIR /home/admin
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
