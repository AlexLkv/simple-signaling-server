from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

connections: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for conn in connections:
                if conn != websocket:
                    await conn.send_text(data)
    except:
        connections.remove(websocket)
