# Day Planner (Django REST API & Ionic/Angular Frontend)

Bem-vindo ao projeto Day Planner! Este aplicativo é uma ferramenta de produtividade pessoal que ajuda os usuários a organizar suas tarefas, anotações e datas importantes. Ele é construído com um backend robusto em Django REST Framework e um frontend mobile/web moderno em Ionic com Angular.

## Visão Geral do Projeto

O Day Planner permite que os usuários:
- Criem e gerenciem categorias de tarefas com itens de lista.
- Registrem anotações detalhadas, com a opção de anexar fotos.
- Adicionem e controlem datas importantes e comemorativas.
- Visualizem um perfil de usuário com estatísticas básicas.
- Realizem login e registro de usuários.

## Funcionalidades Principais

### Backend (Django)
- **Autenticação:** Login, Logout e Registro de usuários usando o sistema de autenticação do Django.
- **Gerenciamento de Tarefas:** CRUD (Criar, Ler, Atualizar, Deletar) para categorias de tarefas (e.g., "Pessoais", "Estudantis"), onde cada categoria pode conter até 9 itens de texto. A prioridade da categoria define sua cor.
- **Gerenciamento de Anotações:** CRUD para anotações com título, tópico, conteúdo, cor de borda e upload de fotos (exibidas na DetailView).
- **Gerenciamento de Datas:** CRUD para datas importantes e comemorativas.
    - Datas Comemorativas são fixas para todos os usuários (exibidas pelo mês e ano atual, não excluíveis pelo usuário).
    - Datas Importantes são específicas do usuário.
- **Propriedade de Dados:** Tarefas, Anotações e Datas são associadas ao usuário logado, garantindo que cada usuário veja apenas seus próprios dados (exceto datas comemorativas fixas).
- **APIs REST:** Endpoints para autenticação e listagem de dados.

### Frontend (Ionic/Angular)
- **Tela de Login:** Autenticação via API Django, com armazenamento de token no `localStorage`.
- **Dashboard (Home):** Exibe um resumo das tarefas (em carrossel), anotações e datas do usuário logado.
- **Navegação por Abas:** (Se implementado) Navegação intuitiva entre seções principais (Tarefas, Anotações, Datas, Perfil).
- **Estilo Responsivo:** Layout adaptável a diferentes tamanhos de tela (mobile, tablet, desktop).

## Tecnologias Utilizadas

### Backend
- **Python 3.x**
- **Django 5.x**
- **Django REST Framework (DRF)**
- **PostgreSQL** (Banco de Dados)
- `django-cors-headers` (Para comunicação entre frontend e backend)

### Frontend
- **Node.js** e **npm**
- **Ionic Framework 8.x**
- **Angular 17.x**
- **TypeScript**

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas em seu ambiente:

-   **Python 3.8+**
-   **pip** (gerenciador de pacotes do Python)
-   **Node.js 18+**
-   **npm 8+**
-   **PostgreSQL** (servidor de banco de dados rodando e acessível)
-   **Ionic CLI** (`npm install -g @ionic/cli`)

## Configuração do Projeto

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.

### 1. Configuração do Backend (Django)

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_DJANGO>
    cd Web
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No Linux/macOS:
    source venv/bin/activate
    ```
3.  **Instale as dependências Python:**
    ```bash
    pip install -r requirements.txt
    # Se não tiver requirements.txt, instale manualmente:
    # pip install Django djangorestframework psycopg2-binary django-cors-headers
    ```
4.  **Configuração do Banco de Dados (PostgreSQL):**
    Certifique-se de que seu servidor PostgreSQL está rodando. Crie um banco de dados e um usuário para o projeto.
    -   **Nome do Banco de Dados:** `agenda`
    -   **Usuário do Banco de Dados:** `gabriel`
    -   **Senha do Banco de Dados:** `1234a`
    -   **Host:** `127.0.0.1` (ou `localhost`)
    -   **Porta:** `5432`

    Se você precisar recriar o banco de dados e dar permissão ao usuário (conecte-se ao `psql` como `postgres`):
    ```sql
    DROP DATABASE IF EXISTS agenda;
    CREATE DATABASE agenda WITH OWNER gabriel;
    ALTER USER gabriel CREATEDB; -- Permissão para criar dbs de teste
    \q
    ```
5.  **Execute as Migrações do Django:**
    Limpe migrações e banco de dados antigos para um estado limpo.
    ```bash
    # (Opcional, mas recomendado se houver problemas de migração ou dados antigos)
    # Exclua a pasta Agenda/migrations/ (exceto __init__.py)
    # Exclua pastas __pycache__ em Agenda/ e DayPlanner/
    # (Se estiver usando SQLite, apague o arquivo db.sqlite3)

    python manage.py makemigrations Agenda
    python manage.py migrate
    ```
6.  **Crie um Superusuário (para acesso ao Admin e para testes):**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Inicie o Servidor Django:**
    ```bash
    python manage.py runserver
    ```
    O backend estará rodando em `http://127.0.0.1:8000/`.

### 2. Configuração do Frontend (Ionic/Angular)

1.  **Navegue para a pasta do projeto Ionic:**
    ```bash
    cd App
    ```
2.  **Instale as dependências Node:**
    ```bash
    npm install
    ```
3.  **Configurar URL da API:**
    No arquivo `src/app/auth/login/login.page.ts` (e em outros componentes que chamam a API), verifique e ajuste a constante `API_BASE_URL`:
    ```typescript
    const API_BASE_URL = '[http://127.0.0.1:8000](http://127.0.0.1:8000)'; // OU SEU IP LOCAL, ex: '[http://192.168.1.100:8000](http://192.168.1.100:8000)'
    ```
4.  **Inicie o Servidor Ionic:**
    ```bash
    ionic serve
    ```
    O frontend estará rodando em `http://localhost:8100/`.

## API Endpoints

A API está disponível no backend Django. Abaixo estão os principais endpoints. Para acessá-los (exceto o de login), você precisará do `token` de autenticação obtido no login.

-   **Base URL:** `http://127.0.0.1:8000/` (ou `http://SEU_IP_AQUI:8000/`)

### Autenticação
-   **Login:** `POST /api/login/`
    -   **Body:** `{"username": "seu_usuario", "password": "sua_senha"}`
    -   **Response:** `{"token": "...", "user_id": ..., "username": "..."}`

### Listagem de Dados (Requer Token na `Authorization` Header: `Token SEU_TOKEN_AQUI`)
-   **Tarefas:** `GET /Agenda/api/tasks/`
-   **Anotações:** `GET /Agenda/api/notes/`
-   **Datas Importantes:** `GET /Agenda/api/dates/`

## Testes

### Testes Unitários (Backend)
Para rodar os testes unitários do backend Django:
``bash
cd Day-Planner
python manage.py test Agenda

## Testes Manuais (Frontend e Backend Integrado)

Para garantir o bom funcionamento da aplicação, siga os passos de teste manual abaixo:

1.  **Acesse o frontend:** Abra seu navegador e navegue até `http://localhost:8100/`.
2.  **Registro:** Crie uma nova conta de usuário acessando a rota `/register`.
3.  **Login:** Faça login na aplicação utilizando a conta que você acabou de criar.
4.  **Navegação:** Verifique se consegue navegar fluentemente entre as diferentes seções do aplicativo:
    * Dashboard (Página inicial)
    * Tarefas
    * Anotações
    * Datas
    * Perfil
5.  **CRUD (Criar, Ler, Atualizar, Deletar):**
    * **Tarefas:** Tente criar novas categorias de tarefas, adicionar itens a elas, editar suas propriedades e excluir categorias existentes.
    * **Anotações:** Crie, visualize, edite e exclua anotações. Teste o upload de fotos.
    * **Datas:** Crie, edite e exclua datas importantes.
    * **Verificação de Datas Comemorativas Fixas:** Confirme que as datas comemorativas fixas (como feriados nacionais) **não podem ser excluídas** pelo usuário.
6.  **Dados por Usuário:**
    * Faça logout.
    * Crie um segundo usuário ou faça login com um usuário diferente.
    * Verifique se este novo usuário não vê os dados (tarefas, anotações, datas importantes gerais) criados pelo primeiro usuário. Cada usuário deve ter seu próprio conjunto de dados.

## Contribuição

Sinta-se à vontade para contribuir para este projeto. Boas-vindas a pull requests, sugestões de melhoria e relatórios de bugs.
