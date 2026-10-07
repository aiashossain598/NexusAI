from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def send(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)


manager = ConnectionManager()
