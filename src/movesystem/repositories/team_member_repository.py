# src/movesystem/repositories/team_member_repository.py

"""Repository de TeamMember (persistência SQLAlchemy)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from movesystem.models.team_member import TeamMember


class TeamMemberRepository:
    """Responsável por operações de persistência do TeamMember."""

    def __init__(self, session: Session) -> None:
        """Recebe uma Session do SQLAlchemy (gerenciada fora do repository)."""
        self._session = session

    def add(self, team_member: TeamMember) -> TeamMember:
        """Insere um TeamMember no banco e retorna o objeto persistido."""
        self._session.add(team_member)
        return team_member

    def get_by_id(self, team_member_id: int) -> TeamMember | None:
        """Busca por ID."""
        return self._session.get(TeamMember, team_member_id)

    def get_by_register(self, register: str) -> TeamMember | None:
        """Busca por registro (único)."""
        stmt = select(TeamMember).where(TeamMember.register == register)
        return self._session.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[TeamMember]:
        """Lista todos os colaboradores ordenados por nome."""
        stmt = select(TeamMember).order_by(TeamMember.name.asc())
        return list(self._session.execute(stmt).scalars().all())

    def search_by_name_or_register(self, value: str) -> list[TeamMember]:
        """Busca por nome (contains) ou por registro (contains), case-insensitive."""
        value = value.strip()
        if not value:
            return []

        like_value = f"%{value}%"

        stmt = (
            select(TeamMember)
            .where(
                (TeamMember.name.ilike(like_value))
                | (TeamMember.register.ilike(like_value))
            )
            .order_by(TeamMember.name.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def delete(self, team_member: TeamMember) -> None:
        """Remove o TeamMember do banco."""
        self._session.delete(team_member)