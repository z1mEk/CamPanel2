#--------------------------------------
# pip install epevermodbus
#--------------------------------------
from epevermodbus.driver import EpeverChargeController
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from general.configLoader import config
from general.deviceManager import device
from datetime import datetime
from general.logger import logging

class pv:
    voltage = 0
    current = 0
    power = 0

class battery:
    voltage = 0
    current = 0
    temp = 0
    soc = 0
    capacity = 0
    charging_equipment_status = None

class load:
    voltage = 0
    current = 0
    power = 0

class data:
    pv = pv
    battery = battery
    load = load
    lastUpdate = None
    
class plugin:

    @classmethod
    async def readData(cls, interval):

        tracer_device = device.FindUsbDevice(config.ePeverTracer.device)
        try:
            tracer = EpeverChargeController(tracer_device, 1)
        except Exception as e:
                logging.error(f"ePeverTracer: {e}")

        while True:
            try:
                #pv
                data.pv.voltage = tracer.get_solar_voltage()
                data.pv.current = tracer.get_solar_current()
                data.pv.power = tracer.get_solar_power()

                #battery
                data.battery.voltage = tracer.get_battery_voltage()
                data.battery.current = tracer.get_battery_current()
                data.battery.soc = tracer.get_battery_state_of_charge()
                data.battery.temp = tracer.get_battery_temperature()
                data.battery.capacity = tracer.get_battery_capacity()
                data.battery.charging_equipment_status = tracer.get_charging_equipment_status()['charging_status']

                #charging_status = {
                #   0: "NO_CHARGING",
                #   1: "FLOAT",
                #   2: "BOOST",
                #   3: "EQUALIZATION",
                #}

                #load
                data.load.voltage = tracer.get_load_voltage()
                data.load.current = tracer.get_load_current()
                data.load.power = tracer.get_load_power()

                data.lastUpdate = datetime.now()   

            except Exception as e:
                logging.error(f"ePeverTracer: {e}")
                #pv
                data.pv.voltage = 20
                data.pv.current = 0
                data.pv.power = 0

                #battery
                data.battery.voltage = 0
                data.battery.current = 0
                data.battery.soc = 0
                data.battery.temp = 0
                data.battery.capacity = 0

                #load
                data.load.voltage = 0
                data.load.current = 0
                data.load.power = 0
            await asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(5))