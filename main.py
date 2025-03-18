from flask import Flask, jsonify
from flask_socketio import SocketIO, emit, join_room
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Hello, this is the SocketIO server running!"

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'You are connected to the server'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('join')
def handle_join(data):
    room = data.get("room", "default")
    join_room(room)
    print(f"Client joined room: {room}")
    emit('message', {'data': f'Joined room: {room}'}, room=room)

@socketio.on('signal')
def handle_signal(data):
    room = data.get("room", "default")
    print(f"Signal received for room {room}: {data}")
    # Передаём сообщение всем, кроме отправителя, в указанную комнату
    emit('signal', data, room=room, include_self=False)

if __name__ == '__main__':
    # Читаем порт из переменной окружения (по умолчанию 5000)
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
