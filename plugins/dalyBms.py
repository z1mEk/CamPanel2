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
    currentFlexUnit = "mA"
    lastUpdate = datetime.now()  

class plugin:

    @classmethod
    async def readSOC(cls, interval):

        bms_device = device.FindUsbDevice(config.dalyBms.device)
        try:
            dalyBms = DalyBMSSinowealth() #if daly BMS chip is Sinowealth
        except Exception as e:
            logging.error(f"DalyBMS: {e}")

        while True:

            try:
                dalyBms.connect(bms_device)
                bms_recv = dalyBms.get_soc()
                dalyBms.disconnect()

                data.RSOC = int(bms_recv['soc_percent'])
                data.current = bms_recv['current']
                data.currentMiliAmper = int(data.current * 1000)
                data.totalVoltage = bms_recv['total_voltage']
                data.currentFlex = (data.currentMiliAmper if abs(data.currentMiliAmper) < 1000 else data.currentMiliAmper / 1000)
                data.currentFlexUnit = ('mA' if abs(data.currentMiliAmper < 1000) else 'A'),
                data.lastUpdate = datetime.now()                
                
            except Exception as e:
                logging.error(f"DalyBMS: {e}")
                data.RSOC = 0
                data.current = 0
                data.currentMiliAmper = 0
                data.totalVoltage = 0
                data.currentFlex = 0
                data.currentFlexUnit = 'mA'
            
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readSOC(2))
