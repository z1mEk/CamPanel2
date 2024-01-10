import nest_asyncio
nest_asyncio.apply()
from general.configLoader import config
from general.deviceManager import device
from serial.serialposix import Serial
from datetime import datetime
from general.logger import logging

class data:
    currentMiliAmper = -452
    totalVoltage = 12.86
    RSOC = 89

    currentFlex = 0
    currentFlexUnit = "A"

    lastUpdate = None

class daly:

    dalySerial = None

    @classmethod
    def reconnect(cls):
        try:
            if cls.dalySerial == None:
                bms_device = device.FindUsbDevice(config.bms.device)
                cls.dalySerial = Serial(bms_device, config.bms.baudrate)
        except Exception as e:
            logging.error(f"DalyBMS: {e}")
            return False
        return True
        
    @classmethod
    #TODO: tu zrobić to co trzeba żeby daly zwracało odpowiednie dane
    def getData(cls):
        buffer = None
        cmd = [0, 0, 0, 0]
        cmd[0] = 0x0a
        cmd[1] = 0x01
        cmd[2] = 0x0f
        cmd[3] = 0x01
        if cls.reconnect():
            cls.dalySerial.write(cmd)
            buffer = cls.dalySerial.read(0x0f)
        return buffer

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            # data.currentMiliAmper = -3456
            # data.totalVoltage = 13.345
            # data.RSOC = 89

            data.currentFlex = (data.currentMiliAmper if abs(data.currentMiliAmper) < 1000 else data.currentMiliAmper / 1000)
            data.currentFlexUnit = ('mA' if data.currentMiliAmper < 1000 else 'A'),

            data.lastUpdate = datetime.now()
            
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(1))
