import serial.tools.list_ports as list_ports
from general.logger import logging

class device():
    def FindUsbDevice(vid_pid):

        logging.info(f"FindUsbDevice({vid_pid})")

        if vid_pid[:4] == "/dev" or vid_pid[:3] == "COM":
            logging.info(f"FindUsbDevice({vid_pid}) -> {vid_pid}")
            return vid_pid
        
        devices = vid_pid.split(':')
        vid = devices[0]
        pid = devices[1]
        #if len(devices) > 2:
        #    snb = devices[3]

        for port in list(list_ports.comports()):
            if port.vid == vid and port.pid == pid: # and (port.serial_number == snb or snb is None):
                logging.info(f"FindUsbDevice({vid_pid}) -> {port.device}")
                return port.device

        return None     