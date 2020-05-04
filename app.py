from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from board import *
from flask_socketio import SocketIO, send, emit
import json
from game import Game


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)



# Somehow need to know what board to connect to.
# Swap out all test_board stuff
@socketio.on('connect')
def get_board():
    # robot = test_board.robots[Color.Red]
    robots = [test_board.robots[Color(i)].get_data() for i in range(1,6)]
    # emit('set board', (test_board.get_json(), robot.get_json()))
    emit('set board', (test_board.get_json(), json.dumps(robots)))


@socketio.on('chat message')
def handle_message(message):
    print('received message: ' + message)
    emit('chat message', message, broadcast=True)


@socketio.on('move robot')
def move_robot(color, direction):
    color = color.title()
    if direction == "up":
        print("up")
        test_board.move_robot(Color[color], Direction.Up)
    elif direction == "right":
        print("right")
        test_board.move_robot(Color[color], Direction.Right)
    elif direction == "down":
        print("down")
        test_board.move_robot(Color[color], Direction.Down)
    else:
        print("left")
        test_board.move_robot(Color[color], Direction.Left)
    robot = test_board.robots[Color[color]]
    emit('robot moved', json.dumps(robot.get_data()), broadcast=True)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/game", methods=['GET','POST'])
def game():
    if request.method == 'GET':
        raise NotImplementedError() # show all games
    else:
        # create new game and a new room using game id as the room name
        game = Game()
        # print(url_for(get_game, game_id=game.id))
        return game.id

@app.route("/game/<game_id>")
def get_game(game_id):
    return render_template('game.html')

