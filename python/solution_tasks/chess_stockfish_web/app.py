# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from stockfish import Stockfish
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'maestro7it-chess-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Глобальное состояние (в продакшене — использовать сессии или БД)
game_state = {
    'engine': None,
    'player_color': 'white',
    'skill_level': 5,
    'initialized': False
}

def init_engine(player_color='white', skill_level=5):
    try:
        # Укажите путь к stockfish.exe, если он не в PATH
        path = os.getenv('STOCKFISH_PATH', None)
        engine = Stockfish(path=path)
        engine.set_skill_level(skill_level)
        engine.set_depth(10)
        game_state.update({
            'engine': engine,
            'player_color': player_color,
            'skill_level': skill_level,
            'initialized': True
        })
        return True
    except Exception as e:
        print(f"Ошибка инициализации Stockfish: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('init_game')
def handle_init(data):
    player_color = data.get('color', 'white')
    skill_level = min(20, max(0, int(data.get('level', 5))))
    
    if init_engine(player_color, skill_level):
        fen = game_state['engine'].get_fen_position()
        emit('game_initialized', {'fen': fen, 'player_color': player_color})
    else:
        emit('error', {'message': 'Не удалось запустить Stockfish'})

@socketio.on('make_move')
def handle_move(data):
    if not game_state['initialized']:
        emit('error', {'message': 'Игра не инициализирована'})
        return

    uci_move = data['move']  # например: 'e2e4'
    engine = game_state['engine']

    if engine.is_move_correct(uci_move):
        engine.make_moves_from_current_position([uci_move])
        fen = engine.get_fen_position()

        # Проверка завершения игры
        if 'mate' in fen:
            emit('game_over', {'result': 'checkmate', 'fen': fen})
            return
        elif 'stalemate' in fen:
            emit('game_over', {'result': 'stalemate', 'fen': fen})
            return

        # Ход Stockfish
        ai_move = engine.get_best_move()
        if ai_move:
            engine.make_moves_from_current_position([ai_move])
            fen = engine.get_fen_position()
            if 'mate' in fen:
                emit('game_over', {'result': 'checkmate', 'fen': fen})
            elif 'stalemate' in fen:
                emit('game_over', {'result': 'stalemate', 'fen': fen})
            else:
                emit('position_update', {'fen': fen})
        else:
            emit('position_update', {'fen': fen})
    else:
        emit('invalid_move', {'move': uci_move})

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5001, debug=True)