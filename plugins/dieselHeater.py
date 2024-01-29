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
        return transmitPacket.pumpFreqMin \
            + (transmitPacket.tempDesired - transmitPacket.tempDesiredMin) \
            / (transmitPacket.tempDesiredMax - transmitPacket.tempDesiredMin) \
            * (transmitPacket.pumpFreqMax - transmitPacket.pumpFreqMin)
    
    @classmethod
    def getErrorDescription(cls, errorState):
        errorMsg = [
            "No Error",
            "No Error, but started",
            "Voltage too low",
            "Voltage too high",
            "Ignition plug failure",
            "Pump Failure - over current",
            "Too hot",
            "Motor Failure",
            "Serial connection lost",
            "Fire is extinguished",
            "Temperature sensor failure"
        ]

        if errorState == 0:
            return "Idle"
        elif errorState == 1:
            return "Running normally"
        else:
            return errorMsg[errorState - 2]
        
    @classmethod
    def getRunStateString(cls, runState):
        runStateStrings = [
            "Off / Standby",
            "Start Acknowledge",
            "Glow plug pre-heat",
            "Failed ignition - pausing for retry",
            "Ignited - heating to full temp phase",
            "Running",
            "Skipped - stop acknowledge",
            "Stopping - Post run glow re-heat",
            "Cooldown"
        ]
        return runStateStrings[runState]

class transmitPacket:
    command: int = 0 # default command
    tempSensor:int = config.dieselHeater.tempSensor * 10 # default or get temperature from BME280
    tempDesired:int = config.dieselHeater.tempDesired * 10
    pumpFreqMin:int = int(config.dieselHeater.pumpFreqMin * 10)
    pumpFreqMax:int = int(config.dieselHeater.pumpFreqMax * 10)
    funSpeedMin:int = config.dieselHeater.funSpeedMin
    funSpeedMax:int = config.dieselHeater.funSpeedMax
    voltageType:int = config.dieselHeater.voltageType
    fanspeedSensor:int = config.dieselHeater.fanspeedSensor
    thermostatMode:int = config.dieselHeater.thermostatMode
    tempDesiredMin:int = config.dieselHeater.tempDesiredMin
    tempDesiredMax:int = config.dieselHeater.tempDesiredMax
    glowPlugPower:int = config.dieselHeater.glowPlugPower
    manualPump:int = config.dieselHeater.manualPump
    altitude:int = config.dieselHeater.altitude # or get altitude from BME280

class data:
    srl:Serial = None
    runState = 0
    runStateString = ""
    errorState = 0
    supplyVoltage = 0
    fanRpm = 0
    fanVoltage = 0
    heatExchTemp = 0
    glowPlugVoltage = 0
    glowPlugCurrent = 0
    actualPumpFreq = 0
    errorCode = 0
    errorDisplay = ""
    errorDescription = ""
    fixedModePumpFreq = 0
    displayGradHzUnit = "Hz"
    displayGradHzValue = ""
    calculateFreq = helper.calculateFrequency()
    lastSend = time.time()

class plugin:
    @classmethod
    def createTransmitPacket(cls):
        frame = b''
        try:
            cmd = [0] * 24
            cmd[0] = 0x76 #Start of Frame - 0x76 for LCD
            cmd[1] = 0x16 #Data Size 24bytes
            cmd[2] = transmitPacket.command #command
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

            frame = b''.join(x.to_bytes(1, 'big') for x in cmd)            

            crc_func = crcmod.predefined.mkPredefinedCrcFun('modbus')
            checksum = crc_func(frame)
            frame += checksum.to_bytes(2, 'big')
            
            transmitPacket.command = 0 # reset command to 0

        except Exception as e:
            logging.error(f"dieselHeater - createTransmitPacket - {e}")

        return frame
       
    @classmethod
    def translateReceivePacket(cls, frame):
        try:
            logging.info(f"{frame}")
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

            data.displayGradHzValue = "{:.0f}".format(transmitPacket.tempDesired / 10) if transmitPacket.thermostatMode == 1 else "{:.1f}".format(data.actualPumpFreq)
            data.displayGradHzUnit = "°C".encode('iso-8859-2', 'replace') if transmitPacket.thermostatMode == 1 else "Hz"
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

                frame_transmit = cls.createTransmitPacket()
                #cls.srl.write(frame_transmit)
                await asyncio.sleep(0.1)
                #frame_receive = cls.srl.read(48) # 48?

                frame_receive = b'\x76\x16\x05\x01\x00\x83\x06\x90\x00\x85\x00\x6A\x00\x82\x03\x85\x0e\x01\x00\x0e\x00\x00\x00\x00\x00'

                cls.translateReceivePacket(frame_receive[:24])
                data.lastSend = time.time()

        except Exception as e:
            logging.error(f"dieselHeater - sendPacket: {e}")

        await asyncio.sleep(0.1)

    @classmethod
    async def sendPacketLoop(cls):
        while True:
            try:
                # if time.time() - data.lastSend < 2:
                #     await asyncio.sleep(3)
                await cls.sendPacket()
                #await asyncio.sleep(interval)
            except Exception as e:
                logging.error(f"dieselHeater - sendPacketLoop - {e}")
            await asyncio.sleep(3)

    @classmethod
    async def start(cls):
            transmitPacket.command = 160
            await cls.sendPacket()

    @classmethod
    async def stop(cls):
            transmitPacket.command = 5
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
