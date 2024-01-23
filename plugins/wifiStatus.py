import asyncio
import subprocess
from general.logger import logging

class data:
    wifiStatus = 0

class plugin:  

    @classmethod
    def wlanUpDown(cls, val):
        if val == 1:
            logging.info("sudo ip link set wlan0 up")
            subprocess.run(["sudo", "ip", "link", "set", "wlan0", "up"])
        else:
            logging.info("sudo ip link set wlan0 down")
            subprocess.run(["sudo", "ip", "link", "set", "wlan0", "down"])

    @classmethod
    def isWlan0Up(cls):
        try:
            result = subprocess.check_output(["sudo", "ip", "link", "show", "wlan0"])
            result_str = result.decode("utf-8")
            data.wifiStatus = 1 if ",UP," in result_str else 0
        except subprocess.CalledProcessError:
            data.wifiStatus = 0

    @classmethod
    async def readData(cls, interval):
        while True:
            cls.isWlan0Up()
            await asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(2))
