# src/movesystem/database/engine.py

"""
Responsabilidade:
- Centralizar a criacao do SQLAlchemy Engine e SessionFactory.
- Evitar que UI/Services conhecam detalhes de conexao (baixo acoplamento).
- Permitir trocar SQLite por outro banco no futuro sem refatorar o sistema inteiro.
"""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def build_sqlite_url(db_file: Path) -> str:
    """
    Responsabilidade:
    - Montar a URL do SQLite de forma consistente.
    - Isolar o formato da URL num unico lugar.
    """
    # NOTE: as_posix() evita problemas de barra invertida no Windows.
    return f"sqlite:///{db_file.as_posix()}"


def get_engine(database_url: str, echo: bool = False) -> Engine:
    """
    Responsabilidade:
    - Criar e retornar o Engine do SQLAlchemy.
    - Engine e thread-safe; pode ser singleton no app.
    """
    return create_engine(
        database_url,
        echo=echo,
        future=True,
    )


def get_session_factory(engine: Engine) -> sessionmaker[Session]:
    """
    Responsabilidade:
    - Criar e retornar a factory de sessions.
    - Sessions NAO sao thread-safe; crie uma por unidade de trabalho (tela/acao).
    """
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True,
    )