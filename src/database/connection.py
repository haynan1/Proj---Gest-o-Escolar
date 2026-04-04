import logging
import os
from pathlib import Path
from typing import Any

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection


LOGGER = logging.getLogger(__name__)
SRC_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SRC_DIR.parent
DEFAULT_DB_PORT = 3306


def _load_environment() -> None:
    """Load environment variables from .env when present.

    In production, system environment variables continue to work even if the
    file does not exist.
    """
    env_path = PROJECT_ROOT / '.env'
    load_dotenv(env_path, override=False)


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(
            "Variáveis de ambiente ausentes para conexão com o banco: "
            f"{name}. Configure o arquivo .env ou as variáveis do sistema."
        )
    return value.strip()


def _get_database_config() -> dict[str, Any]:
    _load_environment()

    host = _get_required_env('DB_HOST')
    user = _get_required_env('DB_USER')
    password = _get_required_env('DB_PASSWORD')
    database = _get_required_env('DB_NAME')

    port_raw = os.getenv('DB_PORT', str(DEFAULT_DB_PORT)).strip()
    try:
        port = int(port_raw)
    except ValueError as exc:
        raise RuntimeError(
            "Valor inválido para DB_PORT. Informe uma porta numérica válida."
        ) from exc

    return {
        'host': host,
        'user': user,
        'password': password,
        'database': database,
        'port': port,
        'charset': 'utf8mb4',
        'use_unicode': True,
        'autocommit': False,
    }


class DatabaseConnection:
    def __init__(self, connection: MySQLConnection):
        self._connection = connection

    def cursor(self, dictionary: bool = False):
        return self._connection.cursor(dictionary=dictionary)

    def execute(self, query: str, params: tuple[Any, ...] | None = None):
        cursor = self.cursor(dictionary=True)
        cursor.execute(query, params or ())
        return cursor

    def commit(self) -> None:
        self._connection.commit()

    def rollback(self) -> None:
        self._connection.rollback()

    def close(self) -> None:
        self._connection.close()


def get_connection() -> DatabaseConnection:
    config = _get_database_config()
    LOGGER.info(
        "Tentando conectar ao banco MySQL/MariaDB em %s:%s, schema '%s'.",
        config['host'],
        config['port'],
        config['database'],
    )

    try:
        connection = mysql.connector.connect(**config)
        return DatabaseConnection(connection)
    except Error as exc:
        raise RuntimeError(
            "Erro ao conectar no banco MySQL/MariaDB. "
            "Verifique host, porta, usuário, senha e nome do banco."
        ) from exc
