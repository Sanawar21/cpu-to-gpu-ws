import asyncio
import websockets
import random
import string
import time


class Message:
    cpu = "TYPE<CPU>"
    gpu = "TYPE<GPU>"

    def identify_as_cpu_client(self):
        return "CLASS<WEBSOCKET_CPU_CLIENT>"

    def identify_as_gpu_client(self, session_id):
        return f"CLASS<WEBSOCKET_GPU_CLIENT><SESSION_ID:{session_id}:>"

    def get_client_type(self, message):
        """
        Returns Message.cpu if message indicates that the user is cpu.
        Returns session_id if message indicates the that the user is gpu.
        Returns None if the message is not indicative (could be data).
        """
        if message == self.identify_as_cpu_client():
            return self.cpu
        else:
            try:
                if "CLASS<WEBSOCKET_GPU_CLIENT><SESSION_ID:" in message:
                    return message.split(":")[-2]
                else:
                    return None
            except:
                return None


class Host:
    def __init__(self) -> None:
        self.sessions = {}
        self._msg = Message()

    def __generate_session_id(self):
        characters = string.ascii_letters + string.digits
        session_key = ''.join(random.choice(characters) for _ in range(8))
        print(session_key)
        return session_key

    def __delete_olds(self):
        to_remove = []
        current_time = time.time()
        for session_id in self.sessions:
            session = self.sessions[session_id]
            # delete the record after 30 mins
            if current_time - session["timestamp"] > 1800:
                to_remove.append(session)
        for session in to_remove:
            del session

    async def __register(self, websocket):
        print(f"{websocket} connected.")
        try:
            async for message in websocket:
                self.__delete_olds()
                client_type = self._msg.get_client_type(message)
                if client_type == self._msg.cpu:  # cpu client initiated a session
                    session_id = self.__generate_session_id()
                    await websocket.send(session_id)
                    self.sessions.update({
                        session_id: {
                            "websocket": websocket,
                            "timestamp": time.time(),
                            "message": None,
                        }
                    })
                elif client_type != None:  # gpu user requests data
                    # client_type here is the session id
                    await websocket.send(self.sessions[client_type]["message"])
                    del self.sessions[client_type]
                else:  # cpu user sent a message
                    for session_id in self.sessions:
                        session = self.sessions[session_id]
                        if session["websocket"] == websocket:
                            session["message"] = message
                            break

        except Exception as e:
            print(e)
        finally:
            print(f"{websocket} disconnected.")

    async def run(self, host="localhost", port="8765"):
        # Start the WebSocket server
        server = await websockets.serve(
            self.__register, host, port
        )
        print(f"WebSocket server started on ws://{host}:{port}")

        # Run the server indefinitely
        await server.wait_closed()


if __name__ == "__main__":
    host_instance = Host()
    asyncio.run(host_instance.run(host="localhost", port=8765))
