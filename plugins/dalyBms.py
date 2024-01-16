import nest_asyncio
nest_asyncio.apply()
from general.configLoader import config
from general.deviceManager import device
from serial.serialposix import Serial
from datetime import datetime
from general.logger import logging
from dalybms import DalyBMSSinowealth

class data:

    bms_device = device.FindUsbDevice(config.bms.device)
    bms = None

    currentMiliAmper = 0
    totalVoltage = 0
    RSOC = 0

    currentFlex = 0
    currentFlexUnit = "A"

    lastUpdate = None

class daly:

    dalySerial = None

    @classmethod
    def reconnect(cls):
        try:
            if data.bms == None:
                bms_device = device.FindUsbDevice(config.bms.device)
                data.bms = DalyBMSSinowealth()
                data.bms.connect(bms_device)
        except Exception as e:
            logging.error(f"DalyBMS: {e}")
            return False
        return True
    

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:

            daly.reconnect()

            bms_recv = data.bms.get_all()
            data.currentMiliAmper = bms_recv['soc']['current'] * 1000
            data.totalVoltage = bms_recv['soc']['total_voltage']
            data.RSOC = int(bms_recv['soc']['soc_percent'])

            data.currentFlex = (data.currentMiliAmper if abs(data.currentMiliAmper) < 1000 else data.currentMiliAmper / 1000)
            data.currentFlexUnit = ('mA' if data.currentMiliAmper < 1000 else 'A'),

            data.lastUpdate = datetime.now()
            
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(1))
