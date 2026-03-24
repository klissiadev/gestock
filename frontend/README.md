# Gestock - Módulo Frontend

Este é o módulo frontend do projeto Gestock, um sistema avançado de gestão de estoque que integra aplicações de LLM (Large Language Models) e Machine Learning. A interface foi desenvolvida para ser rápida, responsiva e de fácil manutenção, utilizando um ecossistema moderno de ferramentas baseadas em React.

> **Vai dar manutenção neste código ou criar novas funcionalidades?** Leia o nosso [Guia de Desenvolvimento](DEVELOPMENT.md) para entender a arquitetura de Features, Services e Tematização (MUI).

## 🚀 Tecnologias Principais

O projeto utiliza as seguintes tecnologias e bibliotecas:

* **Framework principal:** [React 19](https://react.dev/)
* **Build Tool:** [Vite](https://vitejs.dev/) (configurado com Rolldown para otimização de performance)
* **Estilização e Componentes:** 
    * [Material UI (MUI)](https://mui.com/) para componentes de interface
    * Tabelas de dados (`@mui/x-data-grid`)
    * Gráficos (`@mui/x-charts`).
* **Gestão de Estado:** [Zustand](https://github.com/pmndrs/zustand)
* **Navegação:** [React Router DOM](https://reactrouter.com/)
* **Requisições HTTP:** [Fetch API](https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API) (Nativo do navegador)
* **Outras utilidades:** 
    * Manipulação de ícones SVG (`vite-plugin-svgr`)
    * Suporte a Markdown (`react-markdown`) 
    * Uploads via drag-and-drop (`react-dropzone`).

## 📦 Instalação e Execução

Certifica-te de que tens o Node.js instalado na tua máquina.

1. Instala as dependências do projeto:
```bash
npm install
```

2. Executa o servidor de desenvolvimento:
```bash
npm run dev
```

### Outros scripts disponíveis

* `npm run build`: Compila a aplicação para produção.
* `npm run lint`: Executa o ESLint para encontrar e corrigir problemas no código.
* `npm run preview`: Inicia um servidor local para testar a versão de produção gerada após o build.
