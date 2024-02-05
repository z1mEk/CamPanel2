import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from general.configLoader import config
from plugins import dalyBms, relays, epeverTracer
from plugins.hmi import methods as methodsHmi
from general.logger import logging
from datetime import datetime, timedelta
    
class data:
        activeHeating = config.solarWaterHeating.activeHeating

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

        currentHeating = False

class plugin:

    @classmethod
    def isRsocControl(cls):
        if data.RsocControl == 1:
            if dalyBms.data.RSOC >= data.onRsoc:
                return True
            if dalyBms.data.RSOC <= data.offRsoc:
                return False
            return data.currentHeating
        else:
            return True
        
    @classmethod
    def isPvVoltageControl(cls):
        if data.pvVoltageControl == 1:
            if epeverTracer.pv.voltage >= data.onPvVoltage:
                return True
            if epeverTracer.pv.voltage <= data.offPvVoltage:
                return False
            return data.currentHeating
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
            try:
                onHour = datetime.strptime(data.onHour, "%H.%M").time()
                offHour = datetime.strptime(data.offHour, "%H.%M").time()
                now = datetime.now().time()
                if now > onHour and now < offHour:
                    return True
                else:
                    return False
            except Exception as e:
                logging.info(f"isHourControl {e}")
        else:
            return True
    
    @classmethod
    async def autoWaterHeating(cls, interval):
        while True:
            data.currentHeating = (
                data.activeHeating == 1 \
                and cls.isRsocControl() \
                and cls.isRsocControl() \
                and cls.isPvVoltageControl() \
                and cls.isPvPowerControl() \
                and cls.isHourControl()
            )

            if data.currentHeating:
                if relays.data.relay1.val == 0:
                    relays.data.relay1.on() #set on inverter 230V
            
                if relays.data.relay3.val == 0:
                    relays.data.relay3.on() #set on boiler 230V
            else:
                relays.data.relay3.off() #set off boiler 230V

            await asyncio.sleep(interval)   

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.autoWaterHeating(2))