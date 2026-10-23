# ambiente_02 — Servidor + Cliente Linux (Debian 13 no Docker)

Ambiente de treino com **duas máquinas** que se comunicam por uma rede interna:

| | Servidor `Base_Linux` | Cliente `Cliente_Linux` |
|---|---|---|
| Sistema | Debian 13, terminal/CLI | Debian 13 + interface gráfica XFCE |
| Acesso | `docker exec` ou SSH (porta 2222) | Navegador: <http://localhost:6080> |
| Recursos | 1 núcleo · 2 GB RAM | 1 núcleo · 2 GB RAM |
| eth0 | WAN `amb02_wan` 172.31.0.10, com Internet | LAN `amb02_lan` 192.168.200.20, sem Internet |
| eth1 | LAN `amb02_lan` 192.168.200.10 | — |
| Usuários | `admin` / `adm123` (sudo) · `root` / `root123` | `cliente` / `cliente123` (sudo) · `root` / `root123` |

Aplicativos do cliente: Firefox, Mousepad (bloco de notas), Atril (PDF), terminal XFCE,
cliente SSH, FileZilla/lftp/ftp (FTP), telnet, smbclient/Thunar (Samba), TigerVNC Viewer e
Remmina (VNC/RDP), além das ferramentas básicas do sistema.

Na LAN, as máquinas se chamam pelos nomes `servidor` e `cliente`. Por exemplo, no terminal do cliente: `ssh admin@servidor`.

## Requisitos

- Docker Desktop atualizado (Docker Engine 25+) em Windows, macOS ou Linux, com pelo menos 5 GB de RAM reservados
- Python 3.8+ (apenas a biblioteca padrão)
- Portas 2222 e 6080 livres e Internet na primeira execução (cerca de 2 GB de downloads)

## Uso

```bash
cd ambiente_02/scripts
python3 iniciar_ambiente.py              # cria / inicia (Windows: py iniciar_ambiente.py)
python3 finalizar_ambiente.py            # para (mantém os dados)
python3 finalizar_ambiente.py --remover  # exclui containers + redes
python3 finalizar_ambiente.py --tudo     # exclui também as imagens
```

> O nome `Base_Linux` também é usado pelo projeto ambiente_01. Só um dos dois pode existir de cada vez.

## Estrutura

```
docker/servidor/   Dockerfile, entrypoint.sh, motd
docker/cliente/    Dockerfile, entrypoint.sh, supervisord.conf, index.html
scripts/           iniciar_ambiente.py, finalizar_ambiente.py
manuais/           Manual de Comandos, Manual do Ambiente, Tutorial GitHub (.docx) e diagrama
```

Para acessar este repositório privado e baixá-lo, veja [TUTORIAL_GITHUB.md](TUTORIAL_GITHUB.md).

> As senhas são de treino. Troque-as na primeira aula (`passwd` e `sudo passwd root`).
