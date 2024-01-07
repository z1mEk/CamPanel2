import random
import nest_asyncio
nest_asyncio.apply()
import subprocess
from general.config_loader import config

class data:
    wifiStatus = 0
    
class plugin:

    @classmethod
    def enable_wifi():
        subprocess.run(["sudo", "ifconfig", "wlan0", "up"])

    @classmethod
    def disable_wifi():
        subprocess.run(["sudo", "ifconfig", "wlan0", "down"])

    @classmethod
    def check_wifi_connection():
        router_ip = config.wifiStatus.pinghost
        try:
            subprocess.run(["ping", "-c", "1", router_ip], check=True)
            data.wifiStatus = 1
        except subprocess.CalledProcessError:
            data.wifiStatus = 0

    @classmethod
    async def readData(cls, interval):
        while True:
            cls.check_wifi_connection()
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(5))
