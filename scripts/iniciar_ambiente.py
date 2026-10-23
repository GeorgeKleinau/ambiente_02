#!/usr/bin/env python3
"""
Projeto ambiente_02 - Script de INICIALIZACAO (servidor + cliente).

O que faz (idempotente: pode rodar quantas vezes quiser):
  1. Confere o Docker Desktop (versao minima)
  2. Baixa a imagem oficial debian:13 (pull) e testa
  3. Constroi as imagens do servidor e do cliente (pasta ../docker)
  4. Cria as redes  amb02_wan (Internet)  e  amb02_lan (rede interna)
  5. Cria (ou so inicia) os containers Comunicacao_Linux e Cliente_Linux
  6. Testa a comunicacao entre as maquinas e mostra como acessar

Uso:
  python3 iniciar_ambiente.py            # cria/inicia
  python3 iniciar_ambiente.py --rebuild  # reconstroi as imagens antes
"""
import io
import subprocess
import sys
import tarfile
import time
from pathlib import Path

# ---------------- Configuracao do ambiente ----------------
PROJETO = "ambiente_02"
DOCKER_DIR = Path(__file__).resolve().parent.parent / "docker"
IMAGEM_BASE = "debian:13"
VERSAO_MINIMA = 25  # varias redes no 'docker run' exigem Docker Engine 25+

WAN = {"nome": "amb02_wan", "subnet": "172.31.0.0/24", "gateway": "172.31.0.1"}
LAN = {"nome": "amb02_lan", "subnet": "192.168.200.0/24", "gateway": "192.168.200.1"}

SERVIDOR = {
    "nome": "Comunicacao_Linux", "hostname": "comunicacao-linux", "pasta": "servidor",
    "imagem": "ambiente02/comunicacao_linux:debian13",
    "ram": "2g", "cpus": "1",
    # (rede, ip, interface, apelidos DNS)
    "redes": [(WAN, "172.31.0.10", "eth0", []),
              (LAN, "192.168.200.10", "eth1", ["servidor", "comunicacao-linux"])],
    "portas": ["2223:22"],
    "env": [f"WAN_GATEWAY={WAN['gateway']}"],
    "extras": [],
}
CLIENTE = {
    "nome": "Cliente_Linux", "hostname": "cliente-linux", "pasta": "cliente",
    "imagem": "ambiente02/cliente_linux:debian13-xfce",
    "ram": "2g", "cpus": "1",
    "redes": [(LAN, "192.168.200.20", "eth0", ["cliente", "cliente-linux"])],
    "portas": ["6080:6080"],
    "env": [f"LAN_SUBNET={LAN['subnet']}"],
    "extras": ["--shm-size", "512m"],  # o Firefox precisa de memoria compartilhada
}
MAQUINAS = (SERVIDOR, CLIENTE)


def run(cmd, check=True, capture=True, mostrar=True):
    """Executa um comando e devolve o resultado."""
    if mostrar:
        print(f"  $ {' '.join(cmd)}")
    r = subprocess.run(cmd, text=True, capture_output=capture)
    if check and r.returncode != 0:
        print(f"\n[ERRO] {(r.stderr or r.stdout or '').strip()}")
        sys.exit(1)
    return r


def existe(tipo, nome):
    return subprocess.run(["docker", tipo, "inspect", nome],
                          capture_output=True).returncode == 0


def etapa(n, texto):
    print(f"\n[{n}/6] {texto}")


def construir_imagem(maq):
    """docker build enviando o contexto como .tar limpo.
    Evita erro de 'xattr' em discos externos do macOS (arquivos ._* do Finder)
    e converte CRLF -> LF (arquivos baixados/editados no Windows)."""
    pasta = DOCKER_DIR / maq["pasta"]
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as tar:
        for f in sorted(pasta.iterdir()):
            if f.is_file() and not f.name.startswith("._") and f.name != ".DS_Store":
                dados = f.read_bytes().replace(b"\r\n", b"\n")
                info = tarfile.TarInfo(f.name)
                info.size = len(dados)
                info.mode = 0o755 if f.name.endswith(".sh") else 0o644
                tar.addfile(info, io.BytesIO(dados))
    print(f"  $ docker build -t {maq['imagem']} - < (contexto {pasta})")
    r = subprocess.run(["docker", "build", "-t", maq["imagem"], "-"], input=buf.getvalue())
    if r.returncode != 0:
        print(f"\n[ERRO] Falha ao construir {maq['imagem']} (veja as mensagens acima).")
        sys.exit(1)


def projeto_do_container(nome):
    r = run(["docker", "inspect", "-f", '{{index .Config.Labels "projeto"}}', nome],
            check=False, mostrar=False)
    return r.stdout.strip()


def criar_container(maq):
    rede0, ip0, if0, alias0 = maq["redes"][0]

    def net(rede, ip, ifname, aliases):
        s = (f"name={rede['nome']},ip={ip},"
             f"driver-opt=com.docker.network.endpoint.ifname={ifname}")
        return s + "".join(f",alias={a}" for a in aliases)

    cmd = ["docker", "run", "-d", "-it",
           "--name", maq["nome"], "--hostname", maq["hostname"],
           "--label", f"projeto={PROJETO}",
           "--memory", maq["ram"], "--memory-swap", maq["ram"],
           "--cpus", maq["cpus"], "--cpuset-cpus", "0",
           "--cap-add", "NET_ADMIN", "--cap-add", "NET_RAW",
           "--restart", "unless-stopped"]
    for rede in maq["redes"]:
        cmd += ["--network", net(*rede)]
    for p in maq["portas"]:
        cmd += ["-p", p]
    for e in maq["env"]:
        cmd += ["-e", e]
    run(cmd + maq["extras"] + [maq["imagem"]])


def main():
    rebuild = "--rebuild" in sys.argv

    etapa(1, "Verificando Docker Desktop")
    if subprocess.run(["docker", "info"], capture_output=True).returncode != 0:
        print("[ERRO] Docker nao esta rodando. Abra o Docker Desktop e tente de novo.")
        sys.exit(1)
    versao = run(["docker", "version", "--format", "{{.Server.Version}}"]).stdout.strip()
    if int(versao.split(".")[0]) < VERSAO_MINIMA:
        print(f"[ERRO] Docker {versao} e antigo. Atualize o Docker Desktop "
              f"(minimo: Docker Engine {VERSAO_MINIMA}).")
        sys.exit(1)
    print(f"  Docker {versao} OK")
    # Nao reaproveita um container de mesmo nome criado por outro projeto
    for maq in MAQUINAS:
        if existe("container", maq["nome"]):
            dono = projeto_do_container(maq["nome"])
            if dono != PROJETO:
                print(f"[ERRO] Ja existe um container {maq['nome']} de outro projeto "
                      f"({dono or 'desconhecido'}). Remova-o ou renomeie-o antes.")
                sys.exit(1)

    etapa(2, f"Baixando e testando a imagem {IMAGEM_BASE}")
    run(["docker", "pull", IMAGEM_BASE])
    teste = run(["docker", "run", "--rm", IMAGEM_BASE, "grep", "PRETTY_NAME", "/etc/os-release"])
    print(f"  Teste: {teste.stdout.strip()}")

    etapa(3, "Construindo as imagens do servidor e do cliente")
    print("  (a primeira vez pode levar varios minutos; o cliente tem interface grafica)")
    for maq in MAQUINAS:
        if rebuild or not existe("image", maq["imagem"]):
            construir_imagem(maq)
        else:
            print(f"  {maq['imagem']} ja existe (use --rebuild para reconstruir)")

    etapa(4, "Criando redes WAN e LAN")
    for rede in (WAN, LAN):
        if existe("network", rede["nome"]):
            print(f"  {rede['nome']} ja existe")
            continue
        run(["docker", "network", "create", "--driver", "bridge",
             "--label", f"projeto={PROJETO}",
             "--subnet", rede["subnet"], "--gateway", rede["gateway"], rede["nome"]])

    etapa(5, "Criando / iniciando os containers")
    for maq in MAQUINAS:
        if existe("container", maq["nome"]):
            run(["docker", "start", maq["nome"]])
        else:
            criar_container(maq)
    print("  Aguardando os servicos subirem...")
    time.sleep(8)

    etapa(6, "Status e testes")
    for maq in MAQUINAS:
        st = run(["docker", "inspect", "-f", "{{.State.Status}}", maq["nome"]],
                 mostrar=False).stdout.strip()
        ips = run(["docker", "exec", maq["nome"], "ip", "-br", "-4", "addr"],
                  mostrar=False).stdout.strip().splitlines()
        print(f"  {maq['nome']:<14} {st:<8} " + " | ".join(
            " ".join(l.split()[0:3:2]) for l in ips if not l.startswith("lo")))
        for rede, ip, ifname, _ in maq["redes"]:
            linha = next((l for l in ips if l.startswith(ifname)), "")
            if ip not in linha:
                print(f"  [AVISO] {ifname} de {maq['nome']} nao ficou com {ip}; confira com: ip -br addr")
    ping = run(["docker", "exec", CLIENTE["nome"], "ping", "-c", "2", "-W", "2", "servidor"],
               check=False, mostrar=False)
    print("  Cliente -> Servidor (ping servidor): " + ("OK" if ping.returncode == 0 else "FALHOU"))

    print(f"""
======================= AMBIENTE PRONTO =======================
 SERVIDOR Comunicacao_Linux (terminal / SSH)
   Terminal : docker exec -it -u admin Comunicacao_Linux bash
   SSH      : ssh admin@localhost -p 2223      (senha: adm123)
   Root     : su -                             (senha: root123)

 CLIENTE Cliente_Linux (interface grafica XFCE no navegador)
   Navegador: http://localhost:6080            (senha VNC: cliente123)
   Usuario  : cliente / cliente123   |   root / root123

 Do cliente para o servidor: ssh admin@servidor  (ou 192.168.200.10)
 Parar     : python3 finalizar_ambiente.py
===============================================================""")


if __name__ == "__main__":
    main()
