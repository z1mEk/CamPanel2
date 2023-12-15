import serial.tools.list_ports

def find_usb_device_by_vid_pid(vid_pid):
    # Get a list of all available ports
    vid, pid = map(lambda x: int(x, 16), vid_pid.split(':'))

    ports = list(serial.tools.list_ports.comports())

    # Iterate through the ports and find the one with matching VID and PID
    for port in ports:
        print(f"{port.device} - {vid_pid}")
        if port.vid == vid and port.pid == pid:
            return port.device

    # If no matching port is found, return None
    return None