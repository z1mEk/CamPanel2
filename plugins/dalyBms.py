import nest_asyncio
nest_asyncio.apply()

class data:
    currentMiliAmper = 0
    currentAmper = 0
    totalMiliVoltage = 0
    totalVoltage = 0
    remainingCapacity = 0
    temperature = 0
    RSOC = 0

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            data.currentMiliAmper = 5200
            data.currentAmper = data.currentMiliAmper / 1000
            data.totalMiliVoltage = 13250
            data.totalVoltage = data.totalMiliVoltage / 1000
            data.remainingCapacity = 119
            data.temperature = 21
            data.RSOC = 79
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    def initialize(cls, event_loop):     
        event_loop.create_task(cls.readData(1))
