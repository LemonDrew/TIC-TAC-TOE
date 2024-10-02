from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from pentago import create_board, apply_move, check_victory, check_move

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the board
board = create_board()
turn = 1  # Player 1 starts

@app.route('/api/move', methods=['POST'])
def make_move():
    global board
    global turn
    data = request.get_json()
    row, col = data['row'], data['col']

    # Validate move
    if check_move(board, row, col):
        board = apply_move(board, turn, row, col, data.get('rot', 0))
        victory_status = check_victory(board, turn)
        if victory_status:
            return jsonify({'success': True, 'board': board.tolist(), 'victory': turn})  # Send player number
        turn = 2 if turn == 1 else 1  # Switch turns
        return jsonify({'success': True, 'board': board.tolist(), 'victory': None})  # No victory yet

    return jsonify({'success': False, 'message': 'Invalid move'})


if __name__ == '__main__':
    app.run(debug=True) 
