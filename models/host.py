import asyncio
import websockets
import json


class Message:
    def identify_as_cpu_client():
        return "CLASS<WEBSOCKET_CPU_CLIENT>"

    def identify_as_gpu_client(session_id):
        return f"CLASS<WEBSOCKET_GPU_CLIENT><SESSION_ID:{session_id}>"

    def request_status():
        return "GET<STATUS>"


class Host:
    def __init__(self) -> None:
        self.connections = set()
        self.cpu_clients = set()
        self.gpu_clients = set()
        self._msg = Message()

    async def register(self, websocket):
        print(f"{websocket} connected.")
        self.connections.add(websocket)
        try:
            async for message in websocket:
                if message == self._msg.identify_as_cpu_client:
                    self.cpu_clients.add(websocket)
                elif message == self._msg.identify_as_gpu_client:
                    self.gpu_clients.add(websocket)
                else:
                    try:
                        data = json.loads(message)
                        if type(data) == type(dict()):
                            with open("user_responses.txt", "a") as file:
                                file.write(message+"\n")
                    except:
                        pass
        except Exception as e:
            print(e)
        finally:
            self.connections.remove(websocket)
            print(f"{websocket} disconnected.")
