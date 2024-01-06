import websockets
import base64
import json
from .host import Message


class ClientCPU:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.received_messages = []  # List to store received messages

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        print(f"Connected to {self.uri}")

    async def send_data(self, audio_file_path, video_file_path):
        if self.websocket:
            audio_data = open(audio_file_path, "rb")
            video_data = open(video_file_path, "rb")
            audio_encoded = base64.b64encode(audio_data).decode("utf-8")
            video_encoded = base64.b64encode(video_data).decode("utf-8")
            json_object = {
                'audio': audio_encoded,
                'video': video_encoded,
            }
            data = json.dumps(json_object)

            await self.websocket.send(data)
            print(f"Sent data: {data}")

    async def receive_data(self):
        if self.websocket:
            response = await self.websocket.recv()
            print(f"Received data: {response}")
            self.received_messages.append(response)
            return response

    async def listen_for_messages(self):
        while True:
            response = await self.receive_data()

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            print("WebSocket connection closed")
