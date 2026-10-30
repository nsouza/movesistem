# src/movesystem/models/base.py

"""Base declarativa do SQLAlchemy para os models do sistema."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base para todos os models ORM do MoveSystem."""