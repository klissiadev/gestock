# Gestock - Guia de Desenvolvimento do Frontend

Este documento descreve os padrões, a arquitetura e as diretrizes para o desenvolvimento do módulo frontend do **Gestock**. O objetivo é garantir a consistência do código, a facilidade de manutenção e a escalabilidade da interface.

## 🛠️ Tecnologias e Dependências Base

* **Framework:** [React 19](https://react.dev/).
* **Build Tool:** [Vite](https://vitejs.dev/) com o motor de build [Rolldown](https://vite.dev/guide/rolldown) (em fase de transição).
* **Interface (UI):** [Material UI (MUI)](https://mui.com/).
* **Estado Global:** [Zustand](https://github.com/pmndrs/zustand).
* **Navegação:** [React Router DOM](https://reactrouter.com/).
* **Comunicação API:** [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) nativa (não utilizamos Axios).

---

## 📂 Arquitetura do Projeto

O projeto segue uma estrutura baseada em **Features**, onde cada funcionalidade importante do sistema tem seu próprio diretório contendo lógica, componentes e serviços específicos.

```text
src/
├── api/             # Serviços de API globais e auxiliares de autenticação
├── assets/          # Ícones, imagens e recursos estáticos
├── components/      # Componentes reutilizáveis compartilhados (Layout, UI)
├── features/        # Módulos principais (Ex: LLM, Stock, Admin, Upload)
│   └── [FeatureName]/
│       ├── components/ # Componentes específicos desta funcionalidade
│       ├── services/   # Chamadas de API e lógica de negócio
│       ├── hooks/      # Hooks customizados da feature
│       └── pages/      # Views principais que compõem a rota
├── hooks/           # Hooks globais (ex: notificações unread)
├── routes/          # Definições de rotas e proteção de acesso
└── style/           # Tematização do Material UI, paletas e tipografia
```

## 🏗️ Arquitetura de Pastas e Responsabilidades

O projeto segue uma estrutura modular para facilitar o isolamento de funcionalidades:

* **`src/api/`**: Contém os serviços base de comunicação. O ficheiro `LLMAPI.js` centraliza a lógica de *fetch* autenticado e tratamento de erros globais (como o erro 401).
* **`src/features/`**: Cada pasta representa um domínio de negócio (Ex: `LLM`, `stock`, `admin`).
    * **`services/`**: Lógica de chamadas externas exclusiva da funcionalidade.
    * **`pages/`**: Componentes de alto nível que representam as rotas.
    * **`components/`**: Peças de interface específicas do domínio (Ex: `ChatInput.jsx`).
* **`src/hooks/`**: *Hooks* globais, como o `useUnreadNotifications.js`, que gere o estado de alertas em toda a aplicação.
* **`src/style/`**: Centralização da identidade visual via Material UI.

---

## 🔐 Fluxo de Autenticação e Rotas

* **Padrão:** Todas as chamadas devem usar `fetch` nativo.
* **Autenticação:** O token JWT deve ser recuperado do `localStorage` e enviado no cabeçalho `Authorization: Bearer <token>`.
* **Tratamento de Erros:** Implementar redirecionamento automático para `/` (login) em caso de erro `401 (Unauthorized)`.

As rotas são geridas no `AppRoutes.jsx` e protegidas pelo componente `ProtectedRoute`.

### Níveis de Acesso (Roles)
O sistema diferencia as permissões com base no papel do utilizador:
1.  **Gestor (`gestor`)**: Acesso às áreas operacionais: `/home`, `/upload`, `/sheets`, `/notifications`, `/movements`, `/ai`, `/forecast`, `/reports` e `/requests`.
2.  **Administrador (`admin`)**: Acesso a ferramentas de sistema: `/users`, `/register-user`, `/log-imports` e `/log-chats`.

**Nota Técnica:** Todas as rotas autenticadas estão envolvidas pelo `AppLayout`, que fornece a barra lateral e o cabeçalho padrão.



---

## 🤖 Integração com LLM (Minerva)

A lógica do chatbot está concentrada no *hook* `useMinerva.jsx`, que gere o estado complexo das conversas.

### Fluxo de Mensagens e Streaming
* **Sessões:** Se não houver uma sessão ativa ao enviar uma mensagem, o sistema cria uma automaticamente via `createNewSession`.
* **Streaming:** Utilizamos o método `streamMessage` da `llmAPI`. O *hook* utiliza um `TextDecoder` para processar os *chunks* de texto recebidos e atualizar o estado da mensagem do assistente em tempo real, garantindo uma experiência fluida.

---

## 🔔 Sistema de Notificações

As notificações funcionam através de um mecanismo de *polling* (verificação periódica).

* **Polling:** O *hook* `useUnreadNotifications` executa a função `pollNew` a cada 30 segundos (configurável via `pollingInterval`).
* **Gestão de Estado:** Novas notificações são filtradas por ID para evitar duplicados e adicionadas ao topo da lista existente.

---

## 🎨 Tematização e UI (MUI Customization)

Com a remoção do Tailwind, toda a estilização deve ser feita através do motor do Material UI em `src/style/theme.jsx`.

### Padronização de Componentes

O ficheiro `theme.jsx` centraliza os *overrides* globais:
* **Scrollbars:** Estilização personalizada para Chrome, Safari e Firefox aplicada via `MuiCssBaseline` para garantir que as barras de deslocamento não quebrem o layout.
* **Componentes Customizados:** As definições de botões (`MuiButton`), tabelas (`MuiTable`) e campos de texto (`MuiTextField`) estão separadas em ficheiros individuais dentro de `src/style/components/` para facilitar a manutenção.
* **Inputs:** Foco visual e bordas de erro são geridos centralmente para manter a consistência em todos os formulários.

---

## 📡 Padrão de Chamadas API

Todas as funções de serviço devem seguir este modelo de segurança:
1.  Recuperar o token do `localStorage`.
2.  Configurar os headers com `Authorization: Bearer <token>`.
3.  Verificar `response.ok`. Se falhar com status `401`, limpar o token e redirecionar o utilizador para a página de login (`window.location.href = "/"`).

---

## ⚙️ Configuração do Ambiente Local

1. **Instalação:**
   ```bash
   npm install
   ```

2. **Desenvolvimento:**
   ```bash
   npm run dev
   ```

3. **Linter:**
   Utilizamos o ESLint para garantir a qualidade do código. Corra o comando abaixo antes de cada commit:
   ```bash
   npm run lint
   ```