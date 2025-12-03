
## 💻 Pré-requisitos

Este projeto utiliza Poetry para gerenciamento de dependências e ambientes virtuais.
A instalação é feita via pipx, garantindo isolamento e praticidade


* Instalação do PIPX + Poetry

- `pip install --user pipx`
- `pipx install poetry`.
- Ele vai dar uma mensagem de WARNING laranja com um caminho no padrão:
```
WARNING: The script pipx.exe is installed in `<USER folder>\AppData\Roaming\Python\Python3x\Scripts` which is not on PATH
```

- Para adicionar ao caminho PATH:
```
cd <USER folder>\AppData\Roaming\Python\Python3x\Scripts
.\pipx.exe ensurepath
```

* Depois disso: `pipx install poetry`

## 📂 Configuração do Projeto
- Clone o repositório:
```
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
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



