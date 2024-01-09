import nest_asyncio
nest_asyncio.apply()
from general.configLoader import config
from plugins import dalyBms, relays
from general.logger import logging
    
class data:
    active = 1
    minRSOC = config.solarWaterHeating.minRSOC
    minVoltage = config.solarWaterHeating.minVoltage

class plugin:

    @classmethod
    async def autoWaterHeating(cls, interval):
        while True:
            if data.active > 0 and dalyBms.data.RSOC > 80 and dalyBms.data.totalVoltage > data.minVoltage:
                if relays.data.relay1.val == 0:
                    relays.data.relay1.on() #set on inverter 230V
            
                if relays.data.relay3.val == 0:
                    relays.data.relay3.on() #set on boiler 230V
            else:
                relays.data.relay3.off() #set off boiler 230V

            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.autoWaterHeating(5))