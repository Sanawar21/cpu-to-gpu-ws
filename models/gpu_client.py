import websockets
import asyncio
import base64
import json
from host import Message
# from .host import Message


class ClientGPU:
    def __init__(self, host, port, session_id):
        self.host = host
        self.port = port
        self.session_id = session_id
        self.uri = f"ws://{host}:{port}"
        self.__msg = Message()

    async def run_and_download(self, audio_path, video_path):
        async with websockets.connect(self.uri) as websocket:
            print(f"Connected to {self.uri}")
            await websocket.send(self.__msg.identify_as_gpu_client(self.session_id))
            self.data = await websocket.recv()

            json_object = json.loads(self.data)
            audio_encoded = json_object['audio']
            video_encoded = json_object['video']
            audio_data = base64.b64decode(audio_encoded)
            video_data = base64.b64decode(video_encoded)

            with open(audio_path, "wb") as file:
                file.write(audio_data)

            with open(video_path, "wb") as file:
                file.write(video_data)


if __name__ == "__main__":
    client = ClientGPU("localhost", 8765, input("Enter session id: "))
    asyncio.run(client.run_and_download(
        "outputs/download.mp4", "outputs/download.wav"))
