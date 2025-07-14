from fastapi import FastAPI, Request,WebSocket,WebSocketDisconnect
from fastapi.responses import JSONResponse
import asyncio,os,logging
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
import os
import json
from typing import List
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles



load_dotenv()
app = FastAPI()

logging.basicConfig(level = logging.INFO)   
logger = logging.getLogger(__name__)

#Cors header so when a request from frontend comes the browser doesn't says access control not allowed because of absense of cors headers.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can change "*" to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Directory to store session recordings
SESSIONS_DIR = "recordings"
os.makedirs(SESSIONS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/test")
def get_test():
    return FileResponse("static/test.html")

@app.get("/viewer")
def get_viewer():
    return FileResponse("static/viewer.html")

@app.get("/player")
def get_viewer():
    return FileResponse("static/player.html")

@app.post("/record")
async def record_session(request:Request):
    try: 
        data = await request.json()
        session_id = str(uuid.uuid4())
        filename = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        
        with open(filename,"w") as f:
            json.dump(data,f)
            
        return {"status": "success", "session_id": session_id}
    
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    
    
@app.get("/sessions/")
async def get_session():
    path = os.path.join(SESSIONS_DIR)
    files = os.listdir(path)
    sessions = [f for f in files if f.endswith(".json")]
    return JSONResponse(content=sessions)



    
@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Serves the recorded session as JSON for replay."""
    path = os.path.join(SESSIONS_DIR, f"{session_id}")
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"error": "Not found"})

    with open(path, "r") as f:
        data = json.load(f)

    return data 



# Keep track of all  viewers
connected_viewers: List[WebSocket] = []
logger.info(connected_viewers)

@app.websocket("/ws/record")
async def record_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            for viewer in connected_viewers:
                try:
                    await viewer.send_text(data)
                    
                except: 
                    connected_viewers.remove(viewer)
    except WebSocketDisconnect:
        pass


@app.websocket("/ws/view")
async def view_stream(websocket:WebSocket):
    await websocket.accept()
    logger.info("user connected")
    connected_viewers.append(websocket)
    try: 
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_viewers.remove(websocket)