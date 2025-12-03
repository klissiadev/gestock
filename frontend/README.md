# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

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

---
