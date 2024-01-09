import serial.tools.list_ports as list_ports
from general.logger import logging

class device():
    def FindUsbDevice(vid_pid):

        if vid_pid[:4] == "/dev":
            logging.info(f"FindUsbDevice({vid_pid}) -> {vid_pid}")
            return vid_pid

        vid, pid = map(lambda x: int(x, 16), vid_pid.split(':'))

        for port in list(list_ports.comports()):
            if port.vid == vid and port.pid == pid:
                logging.info(f"FindUsbDevice({vid_pid}) -> {port.device}")
                return port.device

        return None