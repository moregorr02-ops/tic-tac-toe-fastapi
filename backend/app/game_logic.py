import random
def check_winner(board: str) -> str | None:
    """Проверяет, есть ли победитель на доске.
    Возвращает 'X', 'O' или None, если победителя нет."""
    lines = [
        [0,1,2], [3,4,5], [6,7,8],  # горизонтали
        [0,3,6], [1,4,7], [2,5,8],  # вертикали
        [0,4,8], [2,4,6]            # диагонали
    ]
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != ' ':
            return board[line[0]]
    return None

def is_board_full(board: str) -> bool:
    """Проверяет, заполнена ли доска."""
    return ' ' not in board

def get_random_move(board: str) -> int | None:
    empty = [i for i, c in enumerate(board) if c == ' ']
    return random.choice(empty) if empty else None