'''
sudo pip3 install w1thermsensor
https://github.com/timofurrer/w1thermsensor
https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
'''
import asyncio
import random

class data:
    temp1 = 0
    temp2 = 0
    temp3 = 0

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:

            await asyncio.sleep(interval)  

    @classmethod
    def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(1))  
