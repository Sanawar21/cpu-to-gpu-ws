import websockets
import asyncio
import base64
import json
from host import Message
# from .host import Message


class ClientCPU:
    def __init__(self):
        self.__websocket = None
        self.session_id = None  # to store session id returned by the host
        self.__msg = Message()

    async def connect(self, host, port):
        uri = f"ws://{host}:{port}"
        self.__websocket = await websockets.connect(uri)
        # await self.__listen_for_messages()
        await self.__websocket.send(self.__msg.identify_as_cpu_client())
        async for msg in self.__websocket:
            self.session_id = msg
            break
        print(f"Connected to {uri}")

    async def send_data(self, audio_file_path, video_file_path):
        if self.__websocket:
            audio_data = open(audio_file_path, "rb")
            video_data = open(video_file_path, "rb")
            audio_encoded = base64.b64encode(audio_data).decode("utf-8")
            video_encoded = base64.b64encode(video_data).decode("utf-8")
            json_object = {
                'audio': audio_encoded,
                'video': video_encoded,
            }
            data = json.dumps(json_object)

            await self.__websocket.send(data)
            print(f"Sent audio and video data.")

    async def __receive_data(self):
        if self.__websocket:
            response = await self.__websocket.recv()
            print(f"Received data: {response}")
            self.session_id = response

    async def __listen_for_messages(self):
        while self.session_id == None:
            await self.__receive_data()

    async def close(self):
        if self.__websocket:
            await self.__websocket.close()
            print("WebSocket connection closed")


if __name__ == "__main__":
    client = ClientCPU()
    asyncio.run(client.connect("localhost", "8765"))
    print(client.session_id)
