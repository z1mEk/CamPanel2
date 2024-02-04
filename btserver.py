import bluetooth
import json

def run_ble_server():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1

    server_sock.bind(("", port))
    server_sock.listen(1)

    print("Oczekiwanie na połączenie...")

    client_sock, client_info = server_sock.accept()
    print("Połączono z", client_info)

    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break

            print(f"Odebrano dane BLE: {data.decode()}")

            # Przykładowa odpowiedź serwera
            response_data = {"nazwisko": "Gabriel Zima"}
            response_json = json.dumps(response_data)
            
            client_sock.send(response_json.encode())

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    finally:
        client_sock.close()
        server_sock.close()

if __name__ == "__main__":
    run_ble_server()