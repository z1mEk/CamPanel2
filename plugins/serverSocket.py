import random
import socket
import inspect
import nest_asyncio
nest_asyncio.apply()
from general.logger import logging
from plugins import dalyBms

class data:
    host = "0.0.0.0"
    port = 12345
    server_socket = None
    client_socket = None
    
class plugin:

    @classmethod
    async def handleCommand(cls, command):
        if command == "print_data":
            return dalyBms.data
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
        data.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data.server_socket.bind((data.host, data.port))
        data.server_socket.listen(1)
        
        while True:
            data.client_socket, addr = data.server_socket.accept()
            logging.INFO(f"Connection from {addr}")

            socket_data = data.client_socket.recv(1024).decode('utf-8').strip()
            response = await event_loop.run_in_executor(None, cls.processCommand, socket_data)
            data.client_socket.send(response.encode('utf-8'))
            data.client_socket.close()    

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.startServerSocket(event_loop))