# Tutorial: como acessar e baixar o ambiente_02 do GitHub

O repositório **https://github.com/GeorgeKleinau/ambiente_02** é **privado**. Só quem foi
convidado consegue vê-lo. Quem não foi convidado recebe a página "404 – Not Found".

## 1. Professor: liberar o acesso para um aluno

1. Abra o repositório no GitHub e clique em **Settings** → **Collaborators** (menu à esquerda).
2. Clique em **Add people**, digite o **usuário do GitHub** ou o e-mail do aluno e confirme.
3. O aluno recebe um convite por e-mail. O convite vale por 7 dias.

Pelo terminal, com o GitHub CLI logado como dono do repositório:

```bash
gh api -X PUT repos/GeorgeKleinau/ambiente_02/collaborators/USUARIO_DO_ALUNO -f permission=pull
```

`permission=pull` dá **apenas leitura**: o aluno baixa, mas não altera o repositório.

Para tirar o acesso: **Settings → Collaborators → Remove**.

## 2. Aluno: aceitar o convite

1. Crie uma conta gratuita em https://github.com/signup, caso ainda não tenha uma.
2. Abra o e-mail **"invited you to collaborate"** e clique em **View invitation**. Outra opção é acessar
   https://github.com/GeorgeKleinau/ambiente_02/invitations.
3. Clique em **Accept invitation**. O repositório passa a abrir normalmente.

## 3. Aluno: baixar o projeto (escolha uma opção)

### Opção A — Baixar ZIP (mais fácil, sem instalar nada)
1. Entre no GitHub com a sua conta e abra https://github.com/GeorgeKleinau/ambiente_02.
2. Clique no botão verde **Code** → **Download ZIP**.
3. Descompacte o arquivo. A pasta se chama `ambiente_02-main`.

### Opção B — Git + GitHub CLI (recomendado, facilita atualizar)
1. Instale o Git (https://git-scm.com) e o GitHub CLI (https://cli.github.com).
   - Windows: `winget install Git.Git GitHub.cli`
   - macOS: `brew install git gh`
   - Debian/Ubuntu: `sudo apt install git gh`
2. Faça login uma única vez. O navegador abre e mostra um código para confirmar:
   ```bash
   gh auth login --hostname github.com --git-protocol https --web
   ```
3. Baixe o projeto:
   ```bash
   gh repo clone GeorgeKleinau/ambiente_02
   ```
   Também funciona `git clone https://github.com/GeorgeKleinau/ambiente_02.git`.
4. Para receber atualizações depois:
   ```bash
   cd ambiente_02
   git pull
   ```

### Opção C — GitHub Desktop (interface gráfica)
1. Instale o GitHub Desktop (https://desktop.github.com) e entre com a sua conta.
2. Escolha **File → Clone repository**, aba **GitHub.com**, selecione `GeorgeKleinau/ambiente_02` e clique em **Clone**.
3. Para atualizar, use **Fetch origin** e depois **Pull origin**.

## 4. Rodar o ambiente

```bash
cd ambiente_02/scripts
python3 iniciar_ambiente.py      # Windows: py iniciar_ambiente.py
```

Depois acesse:
- **Cliente (XFCE):** http://localhost:6080 (senha cliente123)
- **Servidor (SSH):** `ssh admin@localhost -p 2223` (senha adm123)

## Problemas comuns

| Problema | Solução |
|---|---|
| Página 404 ao abrir o repositório | Você não está logado ou ainda não aceitou o convite |
| `Repository not found` no git clone | Faça `gh auth login` com a conta que foi convidada |
| `Authentication failed` / pede senha | O GitHub não aceita a senha da conta no git; use `gh auth login` |
| O convite expirou | Peça ao professor para convidar de novo |
