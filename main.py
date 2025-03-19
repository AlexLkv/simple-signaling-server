import uvicorn
from fastapi import FastAPI
from signaling import app as signaling_app

app = FastAPI()
app.mount("/signaling", signaling_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
