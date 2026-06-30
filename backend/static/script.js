let currentGameId = null;
let board = [];
let currentPlayer = 'X';
let gameStatus = 'ongoing';

const boardElement = document.getElementById('board');
const statusElement = document.getElementById('status');
const messageElement = document.getElementById('message');
const newGameBtn = document.getElementById('new-game-btn');

function renderBoard() {
    boardElement.innerHTML = '';
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement('button');
        cell.className = 'cell';
        cell.dataset.index = i;
        cell.textContent = board[i] === ' ' ? '' : board[i];
        cell.disabled = (gameStatus !== 'ongoing' || board[i] !== ' ');
        if (gameStatus !== 'ongoing' || board[i] !== ' ') {
            cell.classList.add('disabled');
        }
        cell.addEventListener('click', () => onCellClick(i));
        boardElement.appendChild(cell);
    }
}

function updateStatus() {
    if (gameStatus === 'ongoing') {
        statusElement.textContent = `Ход игрока ${currentPlayer}`;
    } else if (gameStatus === 'won') {
        statusElement.textContent = `Победил ${currentPlayer === 'X' ? 'O' : 'X'}!`;
    } else if (gameStatus === 'draw') {
        statusElement.textContent = 'Ничья!';
    }
}

async function createNewGame() {
    // Получаем выбранный режим
    const modeRadio = document.querySelector('input[name="mode"]:checked');
    const mode = modeRadio ? modeRadio.value : 'vs_human';

    try {
        const res = await fetch('/api/games', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: mode })
        });
        const data = await res.json();
        // ... остальное как было
    } catch (err) {
        messageElement.textContent = 'Ошибка создания игры';
    }
}

async function onCellClick(index) {
    if (gameStatus !== 'ongoing' || board[index] !== ' ') return;

    try {
        const res = await fetch(`/api/games/${currentGameId}/moves`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ position: index })
        });
        if (!res.ok) {
            const err = await res.json();
            messageElement.textContent = err.detail || 'Ошибка';
            return;
        }
        const data = await res.json();
        board = data.board.split('');
        currentPlayer = data.current_player;
        gameStatus = data.status;
        renderBoard();
        updateStatus();
        if (gameStatus === 'won') {
            messageElement.textContent = `Победил ${data.winner}!`;
        } else if (gameStatus === 'draw') {
            messageElement.textContent = 'Ничья!';
        }
    } catch (err) {
        messageElement.textContent = 'Ошибка соединения';
    }
}

newGameBtn.addEventListener('click', createNewGame);
createNewGame();