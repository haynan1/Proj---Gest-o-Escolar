# Projeto Gestão Escolar

Aplicação Flask para gerenciamento de escolas, turmas, disciplinas, professores e geração de horários.

## Stack

- Python 3.13+
- Flask
- MySQL 8+ ou MariaDB 10+
- `mysql-connector-python`

## Banco de dados

O projeto está preparado para `MySQL` e `MariaDB`.

Crie o banco antes de iniciar a aplicação:

```sql
CREATE DATABASE gestao_escolar
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

O schema SQL de referência também está disponível em `src/database/schema_mysql.sql`.

## Configuração do ambiente

Crie seu arquivo local a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variáveis com os dados do seu ambiente:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=app_user
DB_PASSWORD=change_me
DB_NAME=gestao_escolar
FLASK_SECRET_KEY=change_this_secret_key
FLASK_DEBUG=1
PORT=5000
```

O arquivo `.env` é apenas local e está ignorado no Git. O arquivo versionado no repositório deve ser somente o `.env.example`.

## Instalação

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Execução

```bash
python3 src/app.py
```

Ao iniciar, a aplicação cria automaticamente as tabelas definidas em `src/database/schema.py`.

## Preparando para o GitHub

- Confira se o `.env` não será versionado.
- Não suba arquivos gerados localmente, como `venv/`, `__pycache__/` e bancos `.db`.
- Se quiser publicar o projeto, basta versionar o código-fonte, o `README.md`, o `.env.example` e o schema SQL.
