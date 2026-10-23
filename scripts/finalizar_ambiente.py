#!/usr/bin/env python3
"""
Projeto ambiente_02 - Script de FINALIZACAO (servidor + cliente).

Uso:
  python3 finalizar_ambiente.py            # apenas PARA os containers (dados mantidos)
  python3 finalizar_ambiente.py --remover  # para e EXCLUI containers + redes
  python3 finalizar_ambiente.py --tudo     # exclui containers + redes + imagens

Remover/tudo pede confirmacao (digite SIM). Para pular: adicione --sim
"""
import subprocess
import sys

PROJETO = "ambiente_02"
CONTAINERS = ["Cliente_Linux", "Comunicacao_Linux"]
REDES = ["amb02_wan", "amb02_lan"]
IMAGENS = ["ambiente02/cliente_linux:debian13-xfce", "ambiente02/comunicacao_linux:debian13", "debian:13"]


def run(cmd):
    print(f"  $ {' '.join(cmd)}")
    r = subprocess.run(cmd, text=True, capture_output=True)
    msg = (r.stdout if r.returncode == 0 else r.stderr).strip()
    if msg:
        print(f"    {msg}")
    return r.returncode == 0


def existe(tipo, nome):
    return subprocess.run(["docker", tipo, "inspect", nome],
                          capture_output=True).returncode == 0


def do_projeto(nome):
    """So mexe em containers com o rotulo projeto=ambiente_02."""
    r = subprocess.run(["docker", "inspect", "-f", '{{index .Config.Labels "projeto"}}', nome],
                       text=True, capture_output=True)
    return r.returncode == 0 and r.stdout.strip() == PROJETO


def confirmar(texto):
    if "--sim" in sys.argv:
        return True
    return input(f"\n{texto} Digite SIM para confirmar: ").strip().upper() == "SIM"


def main():
    remover = "--remover" in sys.argv or "--tudo" in sys.argv
    tudo = "--tudo" in sys.argv

    if subprocess.run(["docker", "info"], capture_output=True).returncode != 0:
        print("[ERRO] Docker nao esta rodando. Abra o Docker Desktop.")
        sys.exit(1)

    meus = [c for c in CONTAINERS if do_projeto(c)]
    for c in CONTAINERS:
        if existe("container", c) and c not in meus:
            print(f"  {c} pertence a outro projeto; nao sera alterado.")

    print("\n[1] Parando os containers")
    for c in meus:
        run(["docker", "stop", c])
    if not meus:
        print("  Nenhum container deste projeto encontrado.")

    if not remover:
        print("\nContainers parados. Os dados foram mantidos.")
        print("Para religar: python3 iniciar_ambiente.py")
        return

    alvo = "containers, redes e imagens" if tudo else "containers e redes"
    if not confirmar(f"ATENCAO: isto vai EXCLUIR {alvo} do {PROJETO}. "
                     "Tudo que foi feito dentro das maquinas sera perdido."):
        print("Cancelado. Nada foi excluido.")
        return

    print("\n[2] Excluindo os containers")
    for c in meus:
        run(["docker", "rm", "-f", c])

    print("\n[3] Excluindo as redes")
    for rede in REDES:
        if existe("network", rede):
            run(["docker", "network", "rm", rede])

    if tudo:
        print("\n[4] Excluindo as imagens")
        for img in IMAGENS:
            if existe("image", img):
                run(["docker", "rmi", img])

    print("\nEstrutura removida.")


if __name__ == "__main__":
    main()
