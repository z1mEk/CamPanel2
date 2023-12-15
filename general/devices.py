import pyudev

def find_usb_device_by_vid_pid(vid_pid):
    # Inicjalizacja obiektu kontekstu udev
    context = pyudev.Context()

    # Uzyskanie listy wszystkich urządzeń USB
    devices = list(context.list_devices(subsystem='tty', ID_BUS='usb'))

    # Parsowanie VID i PID z jednego parametru w postaci "067b:2303"
    vid, pid = map(lambda x: int(x, 16), vid_pid.split(':'))

    # Iteracja przez każde urządzenie w poszukiwaniu pasującego VID i PID
    for device in devices:
        try:
            # Pobranie VID i PID z atrybutów urządzenia
            device_vid = int(device.attributes.asstring('idVendor'), 16)
            device_pid = int(device.attributes.asstring('idProduct'), 16)

            # Sprawdzenie, czy urządzenie ma oczekiwane VID i PID
            if device_vid == vid and device_pid == pid:
                # Znaleziono pasujące urządzenie, zwróć jego ścieżkę (/dev/ttyUSBX)
                return device.device_node
        except (ValueError, KeyError):
            pass

    # Jeśli nie znaleziono pasującego urządzenia, zwróć None
    return None