import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, Depends, WebSocketException, HTTPException
from starlette.websockets import WebSocketDisconnect

from src.auth.auth_handler import decode_jwt
from src.database import get_async_session
from src.db_manager import DBManager
from src.messanger.connect_manager import manager
from src.models.message import Message

router = APIRouter(
    prefix="/chat"
)


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket, access_token: str, session=Depends(get_async_session)):
    print("Try")
    data = decode_jwt(access_token)
    if not data:
        return WebSocketException(401, "Invalid token!")
    print(data)
    await manager.connect(websocket, data["username"])
    await manager.send_personal_message("welcome", data["username"], data["username"])
    try:
        while True:

            data = await websocket.receive_json()
            data = json.loads(data)
            if not ("message" in data and "recipient" in data and "author" in data):
                continue
            await DBManager.create_message(
                session,
                Message(
                    author_username=data["author"],
                    recipient_username=data["recipient"],
                    text=data["message"],
                    date=datetime.now()
                )
            )
            await manager.send_personal_message(data["message"], data["recipient"], data["author"])
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("/get_chat")
async def get_chat(access_token: str, session=Depends(get_async_session)):
    user = decode_jwt(access_token)

    if not user:
        return HTTPException(401, "Invalid token!")
    chats = await DBManager.get_chats(session, user["username"])
    response = {"status_code": 200, "chats": chats}
    return response
