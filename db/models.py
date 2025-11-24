from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Integer,
    String,
    Float,
    Text,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

def now_str() -> str:
    """UTC ISO-8601 string for created_at/updated_at."""
    return datetime.utcnow().isoformat()


class Base(DeclarativeBase):
    """Base for ORM models."""
    pass


class TimestampMixin:
    """Adds created_at/updated_at ISO timestamp strings."""
    created_at: Mapped[str] = mapped_column(String, default=now_str)
    updated_at: Mapped[str] = mapped_column(String, default=now_str)

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = now_str()


class Player(Base, TimestampMixin):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id: Mapped[Optional[str]] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    team: Mapped[Optional[str]] = mapped_column(String)
    position: Mapped[Optional[str]] = mapped_column(String)
    active: Mapped[int] = mapped_column(Integer, default=1)
    height_in: Mapped[Optional[float]] = mapped_column(Float)
    weight_lb: Mapped[Optional[float]] = mapped_column(Float)

    # Relationships
    games: Mapped[List["PlayerGame"]] = relationship(
        back_populates="player", cascade="all, delete-orphan"
    )
    injuries: Mapped[List["Injury"]] = relationship(
        back_populates="player", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Player id={self.id} name={self.name} team={self.team}>"


class Game(Base, TimestampMixin):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id: Mapped[Optional[str]] = mapped_column(String, unique=True)
    season: Mapped[Optional[str]] = mapped_column(String)
    date: Mapped[str] = mapped_column(String, nullable=False)
    home_team: Mapped[str] = mapped_column(String, nullable=False)
    away_team: Mapped[str] = mapped_column(String, nullable=False)
    home_score: Mapped[Optional[int]] = mapped_column(Integer)
    away_score: Mapped[Optional[int]] = mapped_column(Integer)

    # Relationships
    player_games: Mapped[List["PlayerGame"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Game id={self.id} {self.away_team} @ {self.home_team} date={self.date}>"


class Injury(Base, TimestampMixin):
    __tablename__ = "injuries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[Optional[str]] = mapped_column(String)          # "out", "questionable", etc.
    description: Mapped[Optional[str]] = mapped_column(Text)       # e.g., "left ankle sprain"
    start: Mapped[str] = mapped_column(String, nullable=False)     # ISO date/time
    expected_end: Mapped[Optional[str]] = mapped_column(String)
    actual_end: Mapped[Optional[str]] = mapped_column(String)
    source: Mapped[Optional[str]] = mapped_column(String)          # URL or feed source

    # Relationships
    player: Mapped["Player"] = relationship(back_populates="injuries")

    def __repr__(self) -> str:
        return f"<Injury id={self.id} player_id={self.player_id} status={self.status}>"


class PlayerGame(Base, TimestampMixin):
    __tablename__ = "player_games"
    __table_args__ = (
        UniqueConstraint("player_id", "game_id", name="uq_player_game_once"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"), nullable=False
    )
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )

    minutes: Mapped[Optional[float]] = mapped_column(Float)        # decimal minutes
    points: Mapped[int] = mapped_column(Integer, default=0)
    assists: Mapped[int] = mapped_column(Integer, default=0)
    rebounds: Mapped[int] = mapped_column(Integer, default=0)
    steals: Mapped[int] = mapped_column(Integer, default=0)
    blocks: Mapped[int] = mapped_column(Integer, default=0)
    fg_attempts: Mapped[int] = mapped_column(Integer, default=0)
    fg_made: Mapped[int] = mapped_column(Integer, default=0)
    ft_attempts: Mapped[int] = mapped_column(Integer, default=0)
    ft_made: Mapped[int] = mapped_column(Integer, default=0)
    threes_made: Mapped[int] = mapped_column(Integer, default=0)
    turnovers: Mapped[int] = mapped_column(Integer, default=0)
    plus_minus: Mapped[Optional[int]] = mapped_column(Integer)
    fouls: Mapped[int] = mapped_column(Integer, default=0)
    started: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    player: Mapped["Player"] = relationship(back_populates="games")
    game: Mapped["Game"] = relationship(back_populates="player_games")

    # Helper computed properties (not persisted)
    @property
    def fg_pct(self) -> Optional[float]:
        if self.fg_attempts and self.fg_attempts > 0:
            return self.fg_made / float(self.fg_attempts)
        return None

    @property
    def ft_pct(self) -> Optional[float]:
        if self.ft_attempts and self.ft_attempts > 0:
            return self.ft_made / float(self.ft_attempts)
        return None

    def __repr__(self) -> str:
        return f"<PlayerGame id={self.id} player_id={self.player_id} game_id={self.game_id}>"
