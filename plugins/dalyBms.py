from dalybms import DalyBMSSinowealth
import nest_asyncio
nest_asyncio.apply()
from general.configLoader import config
from general.deviceManager import device
from datetime import datetime
from general.logger import logging

class data:
    currentMiliAmper = 0
    current = 0
    totalVoltage = 0
    RSOC = 0
    currentFlex = 0
    currentFlexUnit = "A"
    lastUpdate = None 

class plugin:

    @classmethod
    async def readData(cls, interval):

        bms_device = device.FindUsbDevice(config.bms.device)
        bms = DalyBMSSinowealth()

        while True:

            try:
                bms.connect(bms_device)
                bms_recv = data.bms.get_all()
                bms.disconnect()

                data.RSOC = int(bms_recv['soc']['soc_percent'])
                data.current = bms_recv['soc']['current']
                data.currentMiliAmper = int(data.current * 1000)
                data.totalVoltage = bms_recv['soc']['total_voltage']
                data.currentFlex = (data.currentMiliAmper if abs(data.currentMiliAmper) < 1000 else data.currentMiliAmper / 1000)
                data.currentFlexUnit = ('mA' if data.currentMiliAmper < 1000 else 'A'),
                data.lastUpdate = datetime.now()                
                
            except Exception as e:
                logging.error(f"DalyBMS: {e}")
            
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(2))
