# src/movesystem/app/bootstrap.py

"""Bootstrap do aplicativo: cria dependências (DB, services)."""

from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker

from movesystem.config.settings import get_database_url
from movesystem.database.engine import get_engine, get_session_factory
from movesystem.services.team_member_service import TeamMemberService


def create_session_factory() -> sessionmaker[Session]:
    """Cria e retorna a session_factory baseada no settings do projeto."""
    database_url = get_database_url()
    engine = get_engine(database_url=database_url, echo=False)
    return get_session_factory(engine)


def create_team_member_service() -> TeamMemberService:
    """Cria e retorna o TeamMemberService já pronto para uso."""
    session_factory = create_session_factory()
    return TeamMemberService(session_factory=session_factory)