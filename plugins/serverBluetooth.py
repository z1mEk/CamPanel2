'''
pip3 install pybluez
'''
import nest_asyncio
nest_asyncio.apply()
import bluetooth
import json

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
                print("Otrzymano dane w formie JSON:", received_json)

                # Przykładowa odpowiedź serwera
                response_data = {"status": "success", "message": "Odebrano dane"}
                response_json = json.dumps(response_data)
                await event_loop.sock_sendall(client_sock, response_json.encode('utf-8'))

        except (ConnectionResetError, BrokenPipeError):
            # Obsługa rozłączenia klienta
            print("Rozłączono z klientem.")

        finally:
            client_sock.close()

    @classmethod
    async def start_bluetooth_server(cls, event_loop):
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", bluetooth.PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        bluetooth.advertise_service(server_sock, "CamPanel", service_classes=[bluetooth.SERIAL_PORT_CLASS])

        print(f"Czekam na połączenie na porcie {port}...")

        while True:
            client_sock, client_info = await event_loop.sock_accept(server_sock)
            print(f"Połączono z {client_info}")

            nest_asyncio.asyncio.ensure_future(cls.handle_client(client_sock, event_loop))

    @classmethod
    def initialize(cls, event_loop):
        event_loop.run_until_complete(cls.start_bluetooth_server(event_loop))