# ⚙️ Setup do Backend
## 💻 Pré-requisitos
Este projeto utiliza **Poetry** para gerenciamento de dependências e ambientes virtuais.  
A instalação é feita via **pipx**, garantindo isolamento e praticidade.

### Instalação do PIPX + Poetry
1. Instale o `pipx`:
   ```bash
   pip install --user pipx

2. Instale o poetry:
    ```bash
    pipx install poetry

3. Durante a instalação, pode aparecer um WARNING semelhante a:
    ```bash
    WARNING: The script pipx.exe is installed in <USER folder>\AppData\Roaming\Python\Python3x\Scripts which is not on PATH

4. Para adicionar ao caminho PATH:
    ```bash
    cd <USER folder>\AppData\Roaming\Python\Python3x\Scripts
    .\pipx.exe ensurepath

5. Após isso, instale o Poetry:
    ```bash
    pipx install poetry

6. Habilite o shell do Poetry (para adicionar o comando `poetry shell`):
    ```bash
    pipx inject poetry poetry-plugin-shell

## 📂 Configuração do Projeto
- Clone o repositório:
```
git clone https://github.com/klissiadev/gestock.git
cd backend
```
- Instale as dependências:
`poetry install`
- Ative o ambiente virtual: `poetry shell`
- Execute o projeto: `task run`

## Comandos úteis do Poetry
- instalar dependências: `poetry install`
- Adicionar dependência: `poetry add nome-pacote`
- Remover dependência: `poetry remove nome-pacote`

## Comandos existentes
Os comandos definidos fazem o seguinte:

* `task lint`: Faz a checagem de boas práticas do código python
* `task pre_format`: Faz algumas correções de boas práticas automaticamente
* `task format`: Executa a formatação do código em relação às convenções de estilo de código
* `task run`: executa o servidor de desenvolvimento do FastAPI
ATENÇÃO: PYTEST NAO CONFIGURADO DE FORMA ADEQUADA !!
* `task pre_test`: executa a camada de lint antes de executar os testes
* `task test`: executa os testes com pytest de forma verbosa (-vv) e adiciona nosso código como base de cobertura
* `task post_test`: gera um report de cobertura após os testes

---

## 🧩 Padrão de commits

Usamos **Conventional Commits**:

```
<tipo>(<escopo>): <descrição>
```

**Tipos comuns:**  
`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

**Exemplos:**
```
feat(auth): adicionar login com JWT
fix(user): corrigir NPE ao buscar papeis
docs(readme): instruções de swagger e h2
chore: atualizar dependências do jjwt
```

**Escopos sugeridos:** `auth`, `user`, `admin`, `security`, `config`, `docs`, `build`, `ci`.

---

## 🌱 Fluxo de branches e PRs

**Branches principais:**
- `main`: estável e versionada (merge via PR, protegida)
- `develop`: integração contínua
- `feature/*`: novas funcionalidades (ex.: `feature/auth-refresh-token`)
- `fix/*`: correções (ex.: `fix/security-nullpointer`)
- `chore/*`, `docs/*`, etc.

**Regras de PR:**
- Título em formato Conventional Commits (ex.: `feat(auth): suporte a refresh token (#123)`)
- Descreva objetivo, passos de teste e impacto
- 1 review obrigatório antes do merge
- Preferir **squash merge** para manter histórico limpo
