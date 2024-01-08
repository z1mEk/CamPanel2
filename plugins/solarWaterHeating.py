import nest_asyncio
nest_asyncio.apply()
from general.config_loader import config
from plugins import dalyBms, relays
    
class data:
    active = 1
    minRSOC = 0
    minVoltage = 0

class plugin:

    @classmethod
    async def autoWaterHeating(cls, interval):
        while True:

            data.minRSOC = config.solarWaterHeating.minRSOC
            data.minVoltage = config.solarWaterHeating.minVoltage

            if data.active > 0 and dalyBms.data.RSOC > 80 and dalyBms.data.totalVoltage > data.minVoltage:
                if relays.data.relay1.val == 0:
                    relays.data.relay1.on()
            
                if relays.data.relay3.val == 0:
                    relays.data.relay3.on()
            else:
                relays.data.relay3.off()

            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.autoWaterHeating(5))