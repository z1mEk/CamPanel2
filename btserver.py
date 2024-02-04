import bluetooth

def handle_client(client_sock):
    print("Urządzenie sparowane!")
    client_sock.close()

def main():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1  # Port RFCOMM (Bluetooth)
    
    try:
        server_sock.bind(("", port))
        server_sock.listen(1)
        
        print("Oczekiwanie na połączenie Bluetooth...")
        
        client_sock, address = server_sock.accept()
        print("Połączono z", address)
        
        handle_client(client_sock)
    
    except Exception as e:
        print("Błąd:", e)
    
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()