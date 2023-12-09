import nest_asyncio
nest_asyncio.apply()
import random

class data:
    currentMiliAmper = 0
    currentAmper = 0
    currentDisplay = "0"

    totalMiliVoltage = 0
    totalVoltage = 0
    totalVoltageDisplay = "0"

    remainingCapacity = 0
    temperature = 0

    RSOC = 30
    RSOCDisplay = ""

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            data.currentMiliAmper = -92
            data.currentAmper = data.currentMiliAmper / 1000

            if abs(data.currentMiliAmper) < 1000:
                data.currentDisplay = "{:.0f} mA".format(data.currentMiliAmper)
            elif abs(data.currentAmper) < 10:
                data.currentDisplay = "{:.2f} A".format(data.currentAmper)
            elif abs(data.currentAmper) < 100:
                data.currentDisplay = "{:.1f} A".format(data.currentAmper)
            else:
                data.currentDisplay = "{:.0f} A".format(data.currentAmper)

            data.totalMiliVoltage = 13250
            data.totalVoltage = data.totalMiliVoltage / 1000
            data.totalVoltageDisplay = "{:.2f} V".format(data.totalVoltage)

            data.remainingCapacity = 119

            data.temperature = 21

            data.RSOC = random.randint(1, 100)
            data.RSOCDisplay = "{:.0f}%".format(data.RSOC)
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):     
        event_loop.create_task(cls.readData(1))
