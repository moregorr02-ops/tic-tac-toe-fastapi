from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, game_logic
from .database import SessionLocal

router = APIRouter(prefix="/api", tags=["game"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/games", response_model=schemas.GameResponse)
def create_game(game_data: schemas.GameCreate, db: Session = Depends(get_db)):
    new_game = models.Game(
        board=" " * 9,
        current_player="X",
        status="ongoing",
        mode=game_data.mode
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

@router.get("/games/{game_id}", response_model=schemas.GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.post("/games/{game_id}/moves", response_model=schemas.GameResponse)
def make_move(game_id: int, move: schemas.MoveCreate, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.status != "ongoing":
        raise HTTPException(status_code=400, detail="Game already finished")

    if not (0 <= move.position < 9):
        raise HTTPException(status_code=400, detail="Invalid position")

    if game.board[move.position] != ' ':
        raise HTTPException(status_code=400, detail="Cell already taken")

    board_list = list(game.board)
    board_list[move.position] = game.current_player
    game.board = ''.join(board_list)
    # ... (ход игрока)
# Проверяем победу/ничью после хода игрока
winner = game_logic.check_winner(game.board)
if winner:
    game.status = "won"
    game.winner = winner
elif game_logic.is_board_full(game.board):
    game.status = "draw"
else:
    # Если игра продолжается и это режим с ботом
    if game.mode == "vs_bot":
        # Ход бота (он ходит текущим игроком, т.е. следующим)
        bot_move = game_logic.get_random_move(game.board)
        if bot_move is not None:
            board_list = list(game.board)
            board_list[bot_move] = game.current_player
            game.board = ''.join(board_list)
            # Проверяем победу/ничью после хода бота
            bot_winner = game_logic.check_winner(game.board)
            if bot_winner:
                game.status = "won"
                game.winner = bot_winner
            elif game_logic.is_board_full(game.board):
                game.status = "draw"
            else:
                # Переключаем игрока обратно на человека
                game.current_player = 'X' if game.current_player == 'O' else 'O'
            # Сохраняем ход бота в БД
            bot_move_obj = models.Move(
                game_id=game.id,
                player=game.current_player,  # тот, кто только что сходил (бот)
                position=bot_move
            )
            db.add(bot_move_obj)
        else:
            # Нет свободных клеток – ничья
            game.status = "draw"
    else:
        # Если режим с человеком – просто переключаем игрока
        game.current_player = 'O' if game.current_player == 'X' else 'X'

    winner = game_logic.check_winner(game.board)
    if winner:
        game.status = "won"
        game.winner = winner
    elif game_logic.is_board_full(game.board):
        game.status = "draw"
    else:
        game.current_player = 'O' if game.current_player == 'X' else 'X'

    new_move = models.Move(game_id=game.id, player=game.current_player, position=move.position)
    db.add(new_move)
    db.commit()
    db.refresh(game)
    return game