# src/movesystem/models/team_member.py

"""Model ORM do colaborador (TeamMember)."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from movesystem.models.base import Base


class TeamMember(Base):
    """Representa um colaborador cadastrado no sistema."""

    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True,
        autoincrement=True
    )

    register: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    cost_center: Mapped[str] = mapped_column(String(20), nullable=False)
    supervisor_structure: Mapped[str | None] = mapped_column(String(20), nullable=True)

    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )