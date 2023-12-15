import serial.tools.list_ports

def find_usb_device_by_vid_pid(vid_pid):
    # Parsowanie VID i PID z jednego parametru w postaci "067b:2303"
    vid, pid = map(lambda x: int(x, 16), vid_pid.split(':'))

    # Uzyskanie listy dostępnych portów szeregowych
    ports = list(serial.tools.list_ports.comports())

    # Iteracja przez każdy port w poszukiwaniu pasującego VID i PID
    for port in ports:
        print(port.description)
        try:
            # Pobranie VID i PID z opisu portu
            port_vid, port_pid = map(lambda x: int(x, 16), port.description.split())

            # Sprawdzenie, czy port ma oczekiwane VID i PID
            if port_vid == vid and port_pid == pid:
                # Znaleziono pasujący port, zwróć jego ścieżkę
                return port.device
        except (ValueError, IndexError):
            pass

    # Jeśli nie znaleziono pasującego portu, zwróć None
    return None