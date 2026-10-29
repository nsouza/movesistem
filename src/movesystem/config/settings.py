# src/movesystem/config/settings.py

"""
Responsabilidade:
- Centralizar configuracoes do aplicativo.
- Ser a fonte unica de verdade para paths e URL do banco.
"""

from __future__ import annotations

from pathlib import Path

from movesystem.database.engine import build_sqlite_url

# NOTE: Convencao do projeto: banco SQLite fica em ./data/movesystem.db
# (relativo a raiz do projeto).
DB_FILENAME = "movesystem.db"
DATA_DIRNAME = "data"


def get_project_root() -> Path:
    """
    Responsabilidade:
    - Descobrir a raiz do projeto em tempo de execucao.
    - Evitar caminhos hardcoded no Windows.
    """
    # NOTE: settings.py esta em src/movesystem/config/settings.py
    # Subindo 4 niveis chegamos na raiz do repositorio:
    # settings.py -> config -> movesystem -> src -> <root>
    return Path(__file__).resolve().parents[3]


def get_data_dir() -> Path:
    """
    Responsabilidade:
    - Retornar a pasta ./data e garantir que ela exista.
    """
    data_dir = get_project_root() / DATA_DIRNAME
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_sqlite_db_path() -> Path:
    """
    Responsabilidade:
    - Retornar o caminho completo do arquivo .db do SQLite.
    """
    return get_data_dir() / DB_FILENAME


def get_database_url() -> str:
    """
    Responsabilidade:
    - Retornar a URL do banco no formato aceito pelo SQLAlchemy.
    """
    return build_sqlite_url(get_sqlite_db_path())