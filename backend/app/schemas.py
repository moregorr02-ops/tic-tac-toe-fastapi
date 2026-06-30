from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class GameCreate(BaseModel):
    pass

class MoveCreate(BaseModel):
    position: int

class MoveResponse(BaseModel):
    id: int
    game_id: int
    player: str
    position: int
    timestamp: datetime

    class Config:
        from_attributes = True

class GameResponse(BaseModel):
    id: int
    board: str
    current_player: str
    status: str
    winner: Optional[str] = None
    moves: List[MoveResponse] = []

    class Config:
        from_attributes = True