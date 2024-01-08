import websockets
import asyncio
import base64
import json
from host import Message
# from .host import Message


class ClientCPU:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.uri = f"ws://{host}:{port}"
        self.session_id = None  # to store session id returned by the host
        self.__msg = Message()

    async def run_and_upload(self, audio_path, video_path):
        async with websockets.connect(self.uri) as websocket:
            print(f"Connected to {self.uri}")
            await websocket.send(self.__msg.identify_as_cpu_client())
            self.session_id = await websocket.recv()
            audio_data = open(audio_path, "rb").read()
            video_data = open(video_path, "rb").read()
            audio_encoded = base64.b64encode(audio_data).decode("utf-8")
            video_encoded = base64.b64encode(video_data).decode("utf-8")
            json_object = {
                'audio': audio_encoded,
                'video': video_encoded,
            }
            data = json.dumps(json_object)
            await websocket.send(data)
            return self.session_id


if __name__ == "__main__":
    client = ClientCPU("localhost", 8765)
    asyncio.run(client.run_and_upload(
        "sample_input/audio.wav", "sample_input/video.mp4"))
    print(client.session_id)
