import serial.tools.list_ports as list_ports

class device():
    def FindUsbDevice(vid_pid):

        if vid_pid[:4] == "/dev":
            return vid_pid

        vid, pid = map(lambda x: int(x, 16), vid_pid.split(':'))

        for port in list(list_ports.comports()):
            if port.vid == vid and port.pid == pid:
                return port.device

        return None