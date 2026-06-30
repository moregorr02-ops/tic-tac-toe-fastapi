from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    board = Column(String, default="         ")
    current_player = Column(String, default="X")
    status = Column(String, default="ongoing")
    winner = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    mode = Column(String, default="vs_human")   # <-- ЭТА СТРОКА ДОЛЖНА БЫТЬ

    moves = relationship("Move", back_populates="game")

class Move(Base):
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    player = Column(String)
    position = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    game = relationship("Game", back_populates="moves")