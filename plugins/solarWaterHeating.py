import nest_asyncio
nest_asyncio.apply()
from general.configLoader import config
from plugins import dalyBms, relays, epeverTracer
from general.logger import logging
import datetime
    
class data:
    active = config.solarWaterHeating.active

    RsocControl = config.solarWaterHeating.RsocControl
    onRsoc = config.solarWaterHeating.onRsoc
    offRsoc = config.solarWaterHeating.offRsoc

    pvVoltageControl = config.solarWaterHeating.pvVoltageControl
    onPvVoltage = config.solarWaterHeating.onPvVoltage
    offPvVoltage = config.solarWaterHeating.offPvVoltage

    pvPowerControl = config.solarWaterHeating.pvPowerControl
    minPVPower = config.solarWaterHeating.minPVPower

    hourControl = config.solarWaterHeating.hourControl
    onHour = config.solarWaterHeating.onHour
    offHour = config.solarWaterHeating.offHour


class plugin:

    @classmethod
    def isRsocControl(cls):
        if data.RsocControl == 1:
            if dalyBms.data.RSOC >= data.onRsoc:
                return True
            if dalyBms.data.RSOC <= data.offRsoc:
                return False
        else:
            return True
        
    @classmethod
    def isPvVoltageControl(cls):
        if data.pvVoltageControl == 1:
            if epeverTracer.pv.voltage >= data.onPvVoltage:
                return True
            if epeverTracer.pv.voltage <= data.offPvVoltage:
                return False
        return True
    
    @classmethod
    def isPvPowerControl(cls):
        if data.pvPowerControl == 1:
            if epeverTracer.pv.power >= data.minPVPower:
                return True
            else:
                return False
        return True
        
    @classmethod
    def isHourControl(cls):
        if data.hourControl == 1:
            onHour = datetime.strptime(data.onHour, "%H:%M").time()
            offHour = datetime.strptime(data.offHour, "%H:%M").time()
            now = datetime.now().time()
            if offHour >= now:
                return False
            if onHour >= now:
                return True
        else:
            return True
    
    @classmethod
    async def autoWaterHeating(cls, interval):
        while True:
            if data.active > 0 and cls.isRsocControl() and cls.isRsocControl() and cls.isPvVoltageControl() and cls.isPvPowerControl() and cls.isHourControl():
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