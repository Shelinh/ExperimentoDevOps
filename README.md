# ExperimentoDevOps 
## 🔐 Sistema de Autenticação e Gestão de Usuários (Flask + SQLite)

Aplicação web desenvolvida em Python com o microframework **Flask**, voltada para o gerenciamento de controle de acesso (RBAC - *Role-Based Access Control*), autenticação segura de usuários e operações completas de CRUD (*Create, Read, Update, Delete*).

---

## 🚀 Funcionalidades

- **Autenticação Segura:** Criptografia de senhas utilizando hash unidirecional (`Werkzeug.security`).
- **Controle de Acesso por Perfil:**
  - **Administrador (`admin`):** Acesso completo ao painel de controle, criação, edição e exclusão de usuários.
  - **Usuário Comum (`user`):** Acesso restrito à área comum (`/home`).
- **Persistência de Dados:** Banco de dados relacional **SQLite3** integrado nativamente.
- **Interface Responsiva:** Desenvolvida com **Bootstrap 5** para melhor experiência visual em dispositivos móveis e desktop.
- **Sessões HTTP:** Gerenciamento seguro de estado e controle de rotas protegidas via `Flask Session`.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12+
- **Framework Web:** Flask 3.x
- **Segurança:** Werkzeug
- **Banco de Dados:** SQLite3
- **Front-end:** HTML5, CSS3, Bootstrap 5 (CDN)
- **Ambiente de Desenvolvimento:** GitHub Codespaces / VS Code

---

## 📁 Estrutura do Projeto

```text
LoginSystem/
├── app.py                 # Rotas principais, controle de sessão e lógica da aplicação
├── database.py            # Conexão SQLite e inicialização do schema/admin
├── requirements.txt       # Dependências do projeto
├── static/
│   └── css/
│       └── style.css      # Estilos CSS complementares
└── templates/
    ├── base.html          # Template base com CDN do Bootstrap 5
    ├── login.html         # Tela de autenticação
    ├── home.html          # Área logada para usuário comum
    ├── usuarios.html      # Painel administrativo (Listagem CRUD)
    ├── novo_usuario.html  # Formulário de cadastro
    └── editar_usuario.html# Formulário de edição