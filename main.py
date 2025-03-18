# server.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # Предполагается, что фронтенд собран и размещён

@socketio.on('message')
def handle_message(data):
    # Рассылаем полученные сообщения всем клиентам, кроме отправителя
    emit('message', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
