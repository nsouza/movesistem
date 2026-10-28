# src/movesystem/config/settings.py

"""
Responsabilidade:
- Centralizar configurações do aplicativo.
- Ser a fonte única de verdade para paths e URL do banco.
- Permitir reaproveitar em outros sistemas (mesmo padrão).
"""

from __future__ import annotations

from pathlib import Path


# NOTE: Convenção do projeto:
# Banco SQLite fica em ./data/movesystem.db (relativo à raiz do projeto).
DB_FILENAME = "movesystem.db"
DATA_DIRNAME = "data"


def get_project_root() -> Path:
    """
    Responsabilidade:
    - Descobrir a raiz do projeto em tempo de execução.
    - Evitar caminhos hardcoded em Windows.
    """
    # NOTE: settings.py está em src/movesystem/config/settings.py
    # Subindo 4 níveis chegamos na raiz do repositório:
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
    # Import local para evitar dependência circular em import time.
    from movesystem.infrastructure.db.engine import build_sqlite_url

    return build_sqlite_url(get_sqlite_db_path())