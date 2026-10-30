# src/movesystem/services/team_member_service.py

"""Service de TeamMember (regras e orquestração de persistência)."""

from __future__ import annotations

from datetime import date
from typing import Callable

from sqlalchemy.orm import Session, sessionmaker

from movesystem.models.team_member import TeamMember
from movesystem.repositories.team_member_repository import TeamMemberRepository


class TeamMemberService:
    """Camada de serviço para operações de TeamMember."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        """Recebe a session_factory para abrir sessions por operação."""
        self._session_factory = session_factory

    def save(self, data: dict) -> TeamMember:
        """Cria um novo colaborador e persiste no banco."""
        register = self._normalize_register(data.get("register", ""))
        cost_center = self._normalize_cost_center(data.get("cost_center", ""))

        team_member = TeamMember(
            register=register,
            name=(data.get("name") or "").strip(),
            cost_center=cost_center,
            supervisor_structure=data.get("supervisor_structure"),
            email=(data.get("email") or "").strip() or None,
            date_of_birth=data.get("date_of_birth"),
            is_active=bool(data.get("is_active", True)),
        )

        with self._session_factory() as session:
            repo = TeamMemberRepository(session)
            repo.add(team_member)
            session.commit()
            session.refresh(team_member)

        return team_member

    def update(self, team_member_id: int, data: dict) -> TeamMember:
        """Atualiza um colaborador existente."""
        register = self._normalize_register(data.get("register", ""))
        cost_center = self._normalize_cost_center(data.get("cost_center", ""))

        with self._session_factory() as session:
            repo = TeamMemberRepository(session)
            existing = repo.get_by_id(team_member_id)
            if existing is None:
                raise ValueError("TeamMember não encontrado para atualização.")

            existing.register = register
            existing.name = (data.get("name") or "").strip()
            existing.cost_center = cost_center
            existing.supervisor_structure = data.get("supervisor_structure")
            existing.email = (data.get("email") or "").strip() or None
            existing.date_of_birth = data.get("date_of_birth")
            existing.is_active = bool(data.get("is_active", True))

            session.commit()
            session.refresh(existing)
            return existing

    def delete(self, team_member_id: int) -> None:
        """Exclui um colaborador pelo ID."""
        with self._session_factory() as session:
            repo = TeamMemberRepository(session)
            existing = repo.get_by_id(team_member_id)
            if existing is None:
                return
            repo.delete(existing)
            session.commit()

    def list_all(self) -> list[TeamMember]:
        """Lista todos os colaboradores."""
        with self._session_factory() as session:
            repo = TeamMemberRepository(session)
            return repo.list_all()

    def search_by_name_or_register(self, value: str) -> list[TeamMember]:
        """Busca por nome ou registro (contains)."""
        with self._session_factory() as session:
            repo = TeamMemberRepository(session)
            return repo.search_by_name_or_register(value)

    def _normalize_register(self, value: str) -> str:
        """Normaliza registro removendo máscara e espaços."""
        return (
            (value or "")
            .replace(".", "")
            .replace("/", "")
            .replace("_", "")
            .strip()
        )

    def _normalize_cost_center(self, value: str) -> str:
        """Normaliza centro de custo removendo máscara e espaços."""
        return (value or "").replace(".", "").replace("_", "").strip()