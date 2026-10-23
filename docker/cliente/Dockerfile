# ------------------------------------------------------------------
# Projeto ambiente_02 - CLIENTE Cliente_Linux (Debian 13 + XFCE)
# Desktop grafico leve acessado pelo navegador (noVNC)
# ------------------------------------------------------------------
FROM debian:13

LABEL projeto="ambiente_02" \
      papel="cliente" \
      descricao="Debian 13 com XFCE e ferramentas cliente, acesso via navegador"

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Sao_Paulo \
    LANG=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8

RUN apt-get update && apt-get -y full-upgrade && \
    apt-get install -y --no-install-recommends \
        # --- base do sistema ---
        sudo ca-certificates locales tzdata bash-completion man-db manpages less \
        vim nano curl wget git unzip zip tar xz-utils rsync \
        procps psmisc htop lsof file tree \
        iproute2 iputils-ping net-tools dnsutils traceroute tcpdump \
        netcat-openbsd nmap iptables \
        # --- interface grafica XFCE + acesso pelo navegador ---
        xfce4 xfce4-terminal xfce4-taskmanager xfce4-screenshooter \
        elementary-xfce-icon-theme adwaita-icon-theme fonts-dejavu fonts-noto-color-emoji \
        desktop-base \
        dbus-x11 at-spi2-core xdg-utils \
        tigervnc-standalone-server tigervnc-tools novnc python3-websockify supervisor \
        # --- aplicativos pedidos ---
        mousepad atril ristretto xarchiver \
        firefox-esr firefox-esr-l10n-pt-br \
        openssh-client filezilla lftp ftp \
        telnet smbclient cifs-utils gvfs-backends gvfs-fuse \
        tigervnc-viewer remmina remmina-plugin-rdp remmina-plugin-vnc freerdp3-x11 && \
    sed -i 's/^# *pt_BR.UTF-8/pt_BR.UTF-8/' /etc/locale.gen && locale-gen && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Usuarios: cliente (sudo) e root. Senha do VNC = senha do cliente.
ARG CLIENTE_SENHA=cliente123
ARG ROOT_SENHA=root123
RUN useradd -m -s /bin/bash -G sudo cliente && \
    echo "cliente:${CLIENTE_SENHA}" | chpasswd && \
    echo "root:${ROOT_SENHA}" | chpasswd && \
    mkdir -p /home/cliente/.vnc && \
    echo "${CLIENTE_SENHA}" | vncpasswd -f > /home/cliente/.vnc/passwd && \
    chmod 600 /home/cliente/.vnc/passwd && \
    chown -R cliente:cliente /home/cliente

COPY supervisord.conf /etc/supervisor/conf.d/ambiente.conf
COPY index.html /usr/share/novnc/index.html
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 6080
WORKDIR /home/cliente
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
