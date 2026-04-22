# Projeto Gestao Escolar

Aplicacao Flask para gerenciamento de escolas, turmas, disciplinas, professores e geracao de horarios.

## Stack

- Python 3.13+
- Flask
- MySQL 8+ ou MariaDB 10+
- `mysql-connector-python`
- Autenticacao por sessao com hash seguro de senha

## Banco de dados

O projeto esta preparado para `MySQL` e `MariaDB`.

Se o banco configurado em `DB_NAME` nao existir, a aplicacao tenta cria-lo automaticamente na inicializacao.
O usuario configurado precisa ter permissao para `CREATE DATABASE`.

O schema SQL de referencia tambem esta disponivel em `src/database/schema_mysql.sql`.

## Configuracao do ambiente

Crie seu arquivo local a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variaveis com os dados do seu ambiente:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=app_user
DB_PASSWORD=change_me
DB_NAME=gestao_escolar
FLASK_SECRET_KEY=change_this_secret_key
FLASK_DEBUG=1
PORT=5000
APP_BASE_URL=http://localhost:5000
AUTH_BOOTSTRAP_ADMIN_NAME=Administrador
AUTH_BOOTSTRAP_ADMIN_EMAIL=
AUTH_BOOTSTRAP_ADMIN_PASSWORD=
AUTH_ASSIGN_LEGACY_SCHOOLS_TO_EMAIL=
SESSION_COOKIE_SECURE=0
VERIFY_EMAIL_TOKEN_MAX_AGE=86400
RESET_PASSWORD_TOKEN_MAX_AGE=3600
MAIL_FROM_NAME=EduSchedule
MAIL_FROM_EMAIL=
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_USE_TLS=1
```

O arquivo `.env` e apenas local e esta ignorado no Git. O arquivo versionado no repositorio deve ser somente o `.env.example`.

## Instalacao

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Execucao

```bash
python3 src/app.py
```

Ao iniciar, a aplicacao cria automaticamente as tabelas definidas em `src/database/schema.py`.

## Autenticacao

- O sistema exige login para acessar escolas, dashboards e horarios.
- Novos usuarios podem se cadastrar em `/cadastro`.
- O login usa protecao CSRF, bloqueio temporario apos tentativas invalidas e sessao por cookie.
- A conta precisa confirmar o e-mail antes de entrar.
- Existem fluxos de `reenviar verificacao`, `esqueci senha` e `redefinir senha`.
- As escolas ficam vinculadas ao usuario autenticado, isolando os dados por conta.
- Se quiser subir um usuario administrador inicial automaticamente, preencha:

```env
AUTH_BOOTSTRAP_ADMIN_NAME=Administrador
AUTH_BOOTSTRAP_ADMIN_EMAIL=admin@escola.com
AUTH_BOOTSTRAP_ADMIN_PASSWORD=uma_senha_forte
```

- Ao iniciar a aplicacao, se esse e-mail ainda nao existir, ele sera criado.
- Para bases antigas, as escolas com `user_id` nulo nao sao mais atribuidas automaticamente ao primeiro usuario.
  Use `AUTH_ASSIGN_LEGACY_SCHOOLS_TO_EMAIL` se quiser fazer essa vinculacao de forma explicita e segura.

## Configuracao de e-mail com Gmail

O projeto agora suporta o fluxo basico:

- cadastro com envio de link de verificacao
- reenvio de verificacao
- recuperacao de senha por link

Exemplo de configuracao para Gmail:

```env
APP_BASE_URL=http://localhost:5000
MAIL_FROM_NAME=EduSchedule
MAIL_FROM_EMAIL=seuemail@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seuemail@gmail.com
SMTP_PASSWORD=sua_senha_de_app_do_google
SMTP_USE_TLS=1
```

Observacoes importantes:

- `APP_BASE_URL` define a URL publica usada dentro dos links enviados por e-mail.
- Para Gmail, use senha de app do Google em vez da senha normal da conta.
- Se o SMTP nao estiver configurado, os links continuam sendo registrados no log do servidor para testes locais.
- Se o SMTP estiver configurado, mas o envio falhar, a aplicacao nao cai; ela registra o erro e informa o usuario.

## Preparando para o GitHub

- Confira se o `.env` nao sera versionado.
- Nao suba arquivos gerados localmente, como `venv/`, `__pycache__/` e bancos `.db`.
- Se quiser publicar o projeto, basta versionar o codigo-fonte, o `README.md`, o `.env.example` e o schema SQL.
