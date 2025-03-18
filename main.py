from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, world! Это тестовое приложение для хостинга."

if __name__ == '__main__':
    # Чтение порта из переменной окружения (по умолчанию 5000)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
