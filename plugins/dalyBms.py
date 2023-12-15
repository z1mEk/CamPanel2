import nest_asyncio
nest_asyncio.apply()
from general.config_loader import config
from serial.serialposix import Serial

class data:
    currentMiliAmper = 0
    currentAmper = 0
    currentDisplay = ""

    totalMiliVoltage = 0
    totalVoltage = 0
    totalVoltageDisplay = ""

    RSOC = 0
    RSOCDisplay = ""

class daly:

    dalySerial = None

    @classmethod
    def reconnect(cls):
        try:
            if cls.dalySerial == None:
                cls.dalySerial = Serial(config.bms.com, config.bms.baudrate)
        except Exception as e:
            print(f"Wystąpił problem z połączeniem z modułem BMS: {e}")
            return False
        return True
        
    @classmethod
    #TODO: tu zrobić to co trzeba żeby daly zwracało odpowiednie dane
    def getData(cls):
        buffer = None
        cmd = [0, 0, 0, 0]
        cmd[0] = 0x0a
        cmd[1] = 0x01
        cmd[2] = 0x0f
        cmd[3] = 0x01
        if cls.reconnect():
            cls.dalySerial.write(cmd)
            buffer = cls.dalySerial.read(0x0f)
        return buffer

class plugin:

    @classmethod
    async def readData(cls, interval):
        while True:
            dalyBMSResponse = "" #daly.getData()

            if dalyBMSResponse != None:
                #TODO: przepisać/skonwertować dane z bufora na dane do wyświetlenia
                data.currentMiliAmper = 0
                data.totalMiliVoltage = 0
                data.RSOC = 0                
            else:
                data.currentMiliAmper = -3456
                data.totalMiliVoltage = 13245
                data.RSOC = 89

            data.currentAmper = data.currentMiliAmper / 1000
            if abs(data.currentMiliAmper) < 100:
                data.currentDisplay = "{:.0f} mA".format(data.currentMiliAmper)
            elif abs(data.currentAmper) < 10:
                data.currentDisplay = "{:.2f} A".format(data.currentAmper)
            elif abs(data.currentAmper) < 100:
               data.currentDisplay = "{:.1f} A".format(data.currentAmper)
            else:
               data.currentDisplay = "{:.0f} A".format(data.currentAmper)
            
            data.totalVoltage = data.totalMiliVoltage / 1000
            data.totalVoltageDisplay = "{:.2f} V".format(data.totalVoltage)
                      
            data.RSOCDisplay = "{:.0f}%".format(data.RSOC)
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.readData(1))
