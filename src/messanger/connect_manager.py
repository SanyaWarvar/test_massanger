import json
from typing import List, Dict
from datetime import datetime
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect


class ConnectManager:
    def __init__(self):
        self.active_connection: Dict[str, WebSocket] = {

        }

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        if username in self.active_connection.keys():
            raise ValueError
        self.active_connection[username] = websocket

    def disconnect(self, username: str):
        try:
            del self.active_connection[username]
        except KeyError:
            pass

    async def send_personal_message(self, message: str, username: str, author: str):
        print(self.active_connection)
        json_message = json.dumps({
            "message": message,
            "author": author,
            "date": datetime.now().isoformat()
        })
        await self.active_connection[username].send_json(json_message)

    async def broadcast(self, message: str, author: str, ignore: List[str] = None):
        for username, connection in self.active_connection.items():
            if username is not None and username in ignore:
                continue
            await self.send_personal_message(message, username, author)


manager = ConnectManager()
