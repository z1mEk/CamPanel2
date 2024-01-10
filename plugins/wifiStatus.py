import nest_asyncio
nest_asyncio.apply()
import subprocess
from general.logger import logging

class data:
    wifiStatus = 0

class plugin:  

    @classmethod
    def wlanUpDown(cls, val):
        if val == 1:
            logging.info("sudo ifconfig wlan0 up")
            subprocess.run(["sudo", "ifconfig", "wlan0", "up"])
        else:
            logging.info("sudo ifconfig wlan0 down")
            subprocess.run(["sudo", "ifconfig", "wlan0", "down"])

    @classmethod
    def isWlan0Up(cls):
        try:
            result = subprocess.check_output(["ifconfig", "wlan0"])
            result_str = result.decode("utf-8")
            data.wifiStatus = 1 if "UP" in result_str else 0
        except subprocess.CalledProcessError:
            data.wifiStatus = 0

    @classmethod
    async def readData(cls, interval):
        while True:
            cls.isWlan0Up()
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(10))
