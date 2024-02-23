import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from general.configLoader import config
from general.deviceManager import device
from serial import Serial
from general.logger import logging
import time
import crcmod

class helper:
    @classmethod
    def calculateFrequency(cls):
        return int(transmitPacket.pumpFreqMin \
            + (transmitPacket.tempDesired - transmitPacket.tempDesiredMin) \
            / (transmitPacket.tempDesiredMax - transmitPacket.tempDesiredMin) \
            * (transmitPacket.pumpFreqMax - transmitPacket.pumpFreqMin))
    
    @classmethod
    def getErrorDescription(cls, errorState):
        errorMsg = [
            "Brak błędów",
            "Brak błędów",
            "Za niskie napięcie",
            "Za wysokie napięcie",
            "Awaria świecy żarowej",
            "Awaria pompy",
            "Za wysoka temperatura",
            "Awaria wentylatora",
            "Utracono połączenie szeregowe",
            "Ogień wygaszony",
            "Awaria czujnika temperatury"
        ]

        if errorState == 0:
            return "Idle"
        elif errorState == 1:
            return "Normalna praca"
        else:
            return errorMsg[errorState - 2]
        
    @classmethod
    def getRunStateString(cls, runState):
        runStateStrings = [
            "Wyłączony",
            "Uruchamianie",
            "Rozgrzewanie",
            "Błąd rozpalania",
            "Rozpalony",
            "Praca",
            "Pominięte",
            "Wyłączanie",
            "Schładzanie"
        ]
        return runStateStrings[runState]

class transmitPacket:
    command = 0 # default command
    tempSensor = config.dieselHeater.tempSensor # default or get temperature from BME280
    tempDesired = config.dieselHeater.tempDesired
    pumpFreqMin = int(config.dieselHeater.pumpFreqMin * 10)
    pumpFreqMax = int(config.dieselHeater.pumpFreqMax * 10)
    funSpeedMin = config.dieselHeater.funSpeedMin
    funSpeedMax = config.dieselHeater.funSpeedMax
    voltageType = config.dieselHeater.voltageType
    fanspeedSensor = config.dieselHeater.fanspeedSensor
    thermostatMode = config.dieselHeater.thermostatMode
    tempDesiredMin = config.dieselHeater.tempDesiredMin
    tempDesiredMax = config.dieselHeater.tempDesiredMax
    glowPlugPower = config.dieselHeater.glowPlugPower
    manualPump = config.dieselHeater.manualPump
    altitude = config.dieselHeater.altitude # or get altitude from BME280       

class data:
    srl:Serial = None
    onOff = 0
    runState = 0
    runStateString = ""
    errorState = 0
    supplyVoltage = 0
    fanRpm = 0
    fanVoltage = 0
    heatExchTemp = 0
    glowPlugVoltage = 0
    glowPlugCurrent = 0.0
    actualPumpFreq = 0
    errorCode = 0
    errorDisplay = ""
    errorDescription = ""
    fixedModePumpFreq = 0
    valueDisplay = ""
    calculateFreq = helper.calculateFrequency() / 10
    lastSend = time.time()
    errorCode = 0

class plugin:
    @classmethod
    async def createTransmitPacket(cls):
        try:
            cmd = [0] * 24
            cmd[0] = 0x76 #Start of Frame - 0x76 for LCD
            cmd[1] = 0x16 #Data Size 22bytes
            cmd[2] = transmitPacket.command #command 00h / 05h (stop) / A0h (start)
            cmd[3] = transmitPacket.tempSensor if transmitPacket.thermostatMode == 1 else 0 #temp sensor
            cmd[4] = transmitPacket.tempDesired #desired temp
            cmd[5] = transmitPacket.pumpFreqMin #Minimum Pump frequency
            cmd[6] = transmitPacket.pumpFreqMax #Maximum Pump frequency
            cmd[7], cmd[8] = transmitPacket.funSpeedMin.to_bytes(2, byteorder='big') #Minimum fan speed MSB, LSB
            cmd[9], cmd[10] = transmitPacket.funSpeedMax.to_bytes(2, byteorder='big') #Maximum fan speed MSB, LSB
            cmd[11] = transmitPacket.voltageType #Heater Operating Voltage 
            cmd[12] = transmitPacket.fanspeedSensor #Fan speed sensor
            cmd[13] = 0x32 if transmitPacket.thermostatMode == 1 else 0xCD  #Thermostat/Fixed mode, cmd[3] = 0 when fixed mode
            cmd[14] = transmitPacket.tempDesiredMin #Lower temperature limit
            cmd[15] = transmitPacket.tempDesiredMax #Upper temperature limit
            cmd[16] = transmitPacket.glowPlugPower #Glow Plug Power
            cmd[17] = transmitPacket.manualPump #Manual pump (fuel prime) 0x5A
            cmd[18], cmd[19] = 0xEB, 0x47 #unknown 0xEB MSB and 0x47 LSB for LCD controller
            cmd[20], cmd[21] = transmitPacket.altitude.to_bytes(2, byteorder='big') #Altitude MSB, LSB

            frame = bytes(cmd)

            crc_func = crcmod.predefined.mkPredefinedCrcFun('modbus')
            checksum = crc_func(frame)
            frame += checksum.to_bytes(2, 'big')
            
            transmitPacket.command = 0 # reset command to 0

        except Exception as e:
            logging.error(f"dieselHeater - createTransmitPacket - {e}")

        return frame
       
    @classmethod
    async def translateReceivePacket(cls, frame):
        try:
            data.runState = frame[2]
            data.runStateString = helper.getRunStateString(data.runState)
            data.errorState = frame[3]
            data.supplyVoltage = int.from_bytes(frame[4:6], 'big') / 10
            data.fanRpm = int.from_bytes(frame[6:8], 'big')
            data.fanVoltage = int.from_bytes(frame[8:10], 'big') / 10
            data.heatExchTemp = int.from_bytes(frame[10:12], 'big')
            data.glowPlugVoltage = int.from_bytes(frame[12:14], 'big') / 10
            data.glowPlugCurrent = int.from_bytes(frame[14:16], 'big') / 100
            data.actualPumpFreq = frame[16] / 10
            data.errorCode = frame[17] - 1
            data.errorDisplay = 'E-{:02}'.format(data.errorCode)
            data.errorDescription = helper.getErrorDescription(data.errorState)
            data.fixedModePumpFreq = frame[19]        
            data.valueDisplay = "OFF" if data.runState == 0 else "{:.0f}°C".format(transmitPacket.tempDesired) \
                    if transmitPacket.thermostatMode == 1 else "{:.1f}Hz".format(helper.calculateFrequency() / 10)
        except Exception as e:
            logging.error(f"dieselHeater - translateReceivePacket: {e}")

    @classmethod
    async def sendPacket(cls):
        try:
            # if cls.srl is None:
            #     dieselHeaterDevice = device.FindUsbDevice(config.dieselHeater.device)
            #     cls.srl = Serial(dieselHeaterDevice, 25000)
            # if cls.srl.closed:
            #     cls.srl.open()
            frame_transmit = await cls.createTransmitPacket()
            #cls.srl.write(frame_transmit)
            await asyncio.sleep(0.1)
            #frame_receive = cls.srl.read(48) # 48?

            cmd = [0] * 48
            cmd[24] = 118
            cmd[25] = 22
            cmd[26] = 5
            cmd[27] = 1
            cmd[28] = 0
            cmd[29] = 131
            cmd[30] = 6
            cmd[31] = 144
            cmd[32] = 0
            cmd[33] = 133
            cmd[34] = 0
            cmd[35] = 106
            cmd[36] = 0
            cmd[37] = 130
            cmd[38] = 3
            cmd[39] = 125
            cmd[40] = helper.calculateFrequency() #14
            cmd[41] = 1
            cmd[42] = 0
            cmd[43] = 14
            cmd[44] = 0
            cmd[45] = 0
            cmd[46] = 0
            cmd[47] = 0

            frame_receive = bytes(cmd)
            await cls.translateReceivePacket(frame_receive[24:])

            data.lastSend = time.time()

        except Exception as e:
            logging.error(f"dieselHeater - sendPacket: {e}")

    @classmethod
    async def sendPacketLoop(cls):
        while True:
            try:
                if time.time() - data.lastSend < 0.3:
                     await asyncio.sleep(0.7)
                await cls.sendPacket()
            except Exception as e:
                logging.error(f"dieselHeater - sendPacketLoop - {e}")

    @classmethod
    async def start(cls):
        transmitPacket.command = 0xA0
        await cls.sendPacket()

    @classmethod
    async def stop(cls):
        transmitPacket.command = 0x05
        await cls.sendPacket()

    @classmethod
    async def up(cls):
        if transmitPacket.tempDesired < transmitPacket.tempDesiredMax:
            transmitPacket.tempDesired += 1
            await cls.sendPacket()

    @classmethod
    async def down(cls):
        if transmitPacket.tempDesired > transmitPacket.tempDesiredMin:
            transmitPacket.tempDesired -= 1
            await cls.sendPacket()
   
    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(cls.sendPacketLoop())
