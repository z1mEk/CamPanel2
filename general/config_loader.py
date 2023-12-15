import json
from types import SimpleNamespace
import serial.tools.list_ports as list_ports

with open('./config/config.json') as json_file:
    config = json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))

class configHelper():
    def FindUsbDeviceByVidPid(vid_pid):
        vid, pid = map(lambda x: int(x, 16), vid_pid.split(':'))

        for port in list(list_ports.comports()):
            if port.vid == vid and port.pid == pid:
                return port.device

        return None