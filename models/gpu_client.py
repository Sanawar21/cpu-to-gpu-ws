import asyncio
import json
import websockets
from .host import Message


class ClientGPU:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self._msg = Message()

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        print(f"Connected to {self.uri}")

    async def send_session_id(self, session_id):
        if self.websocket:
            await self.websocket.send(self._msg.identify_as_gpu_client(session_id))
            print(f"Sent data: {self._msg.identify_as_gpu_client(session_id)}")

    async def receive_data(self):
        if self.websocket:
            response = await self.websocket.recv()
            json_object = json.loads(response)
            audio_data, video_data = json_object["audio"], json_object["video"]

            return response

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            print("WebSocket connection closed")
