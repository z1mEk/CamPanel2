import socket
import inspect
import asyncio
from general.logger import logging
from plugins import dalyBms
import json

class data:
    host = "0.0.0.0"
    port = 12345
    server_socket = None
    client_socket = None
    
class plugin:

    @classmethod
    async def handleCommand(cls, command):
        if command == "print_data":
            print(f"{command}")
            return json.dump(dalyBms.data)
        # elif command == "call_async_method":
        #     return await YourClass.your_async_method()
        # elif command == "call_sync_method":
        #     return YourClass.your_sync_method()
        else:
            return "Unknown command"

    @classmethod
    async def processCommand(cls, command):
        try:
            return await cls.handleCommand(command)
        except Exception as e:
            return f"Error: {str(e)}"

    @classmethod
    async def startServerSocket(cls, event_loop):
        print(f"socket.socket")
        data.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"bind")
        data.server_socket.bind((data.host, data.port))
        print(f"listen")
        data.server_socket.listen(1)
        
        while True:
            print(f"socket.accept")
            data.client_socket, addr = data.server_socket.accept()
            print(f"Connection {addr}")

            socket_data = data.client_socket.recv(1024).decode('utf-8').strip()
            print(f"socket_data {socket_data}")
            response = await cls.processCommand(socket_data)

            print(f"response {response}")
            data.client_socket.send(response.encode('utf-8'))
            data.client_socket.close()  
            await asyncio.sleep(1)   


    @classmethod
    async def initialize(cls, event_loop):
        logging.info(f"serverSocketInitialize")
        event_loop.create_task(cls.startServerSocket(event_loop))