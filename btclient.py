import bluetooth
import json

def run_ble_client():
    server_address = "02:11:23:34:86:E2"  # Wstaw rzeczywisty adres MAC serwera Bluetooth
    port = 1

    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_sock.connect((server_address, port))

    try:
        while True:
            # Przykładowe dane JSON do wysłania
            data_to_send = "D2:03:00:80:00:29:96:5F"

            # Wysyłanie danych do serwera
            client_sock.send(json.dumps(data_to_send).encode())

            # Oczekiwanie na odpowiedź od serwera
            response_data = client_sock.recv(1024)
            print(f"Odebrano odpowiedź od serwera: {response_data.decode()}")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    finally:
        client_sock.close()

if __name__ == "__main__":
    run_ble_client()