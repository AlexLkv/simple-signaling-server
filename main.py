from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit, join_room
import os

app = Flask(__name__, static_folder='build')  # предполагается, что React собран в папке build
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Отдаём React‑приложение
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Событие для подключения в комнату (например, для пары пользователей)
@socketio.on('join')
def on_join(data):
    room = data.get('room')
    join_room(room)
    emit('joined', {'msg': f'Joined room: {room}'}, room=room)

# Передача сигнальных сообщений для WebRTC (SDP, ICE)
@socketio.on('signal')
def on_signal(data):
    room = data.get('room')
    emit('signal', data, room=room, include_self=False)

# Передача команд для управления ESP (например, "toggle" для переключения светодиода)
@socketio.on('esp_control')
def on_esp_control(data):
    room = data.get('room')
    emit('esp_control', data, room=room, include_self=False)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)

