'''
pip3 install pybluez

https://stackoverflow.com/questions/37913796/bluetooth-error-no-advertisable-device
https://forums.raspberrypi.com/viewtopic.php?t=132470
'''
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
import bluetooth
from threading import Thread
import subprocess
import json
from general.logger import logging

class data:
    val1 = None
    val2 = None
    
class plugin:

    @classmethod
    async def handle_client(cls, client_sock, event_loop):
        try:
            while True:
                data = await event_loop.sock_recv(client_sock, 1024)
                if not data:
                    break

                # Przetwarzanie odebranych danych w formie JSON
                received_json = json.loads(data.decode('utf-8'))
                logging.info("Otrzymano dane w formie JSON:", received_json)

                # Przykładowa odpowiedź serwera
                response_data = {"status": "success", "message": "Odebrano dane"}
                response_json = json.dumps(response_data)
                await event_loop.sock_sendall(client_sock, response_json.encode('utf-8'))

        except (ConnectionResetError, BrokenPipeError):
            # Obsługa rozłączenia klienta
            logging.info("Rozłączono z klientem.")

        finally:
            client_sock.close()

    @classmethod
    async def start_bluetooth_server(cls, event_loop):
        try:
            server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            server_sock.bind(("", bluetooth.PORT_ANY))
            server_sock.listen(1)
            port = server_sock.getsockname()[1]

            bluetooth.advertise_service(server_sock, "CamPanel2", service_classes=[bluetooth.SERIAL_PORT_CLASS])

            logging.info(f"Czekam na połączenie na porcie {port}...")

            while True:
                client_sock, client_info = await event_loop.sock_accept(server_sock)
                logging.info(f"Połączono z {client_info}")

                asyncio.create_task(cls.handle_client(client_sock, event_loop))
        except Exception as e:
            logging.error(f"start_bluetooth_server - {e}")

    @classmethod
    async def initialize(cls, event_loop):
        subprocess.run(["sudo", "hciconfig", "hci0", "piscan"])
        asyncio.sleep(2)
        thread = Thread(target=cls.tart_bluetooth_server(event_loop))
        thread.daemon = True
        thread.start()
