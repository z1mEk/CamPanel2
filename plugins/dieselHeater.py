import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from general.configLoader import config
from general.deviceManager import device
from serial import Serial
from general.logger import logging
import time

class modbusCRC:
    CRCTableHigh = [
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
            0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
            0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
            0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81,
            0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
            0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
            0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
            0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
            0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
            0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
            0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
            0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
            0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
            0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
            0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
            0x40
        ]

    CRCTableLow = [
            0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06, 0x07, 0xC7, 0x05, 0xC5, 0xC4,
            0x04, 0xCC, 0x0C, 0x0D, 0xCD, 0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09,
            0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A, 0x1E, 0xDE, 0xDF, 0x1F, 0xDD,
            0x1D, 0x1C, 0xDC, 0x14, 0xD4, 0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3,
            0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3, 0xF2, 0x32, 0x36, 0xF6, 0xF7,
            0x37, 0xF5, 0x35, 0x34, 0xF4, 0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A,
            0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28, 0xE8, 0xE9, 0x29, 0xEB, 0x2B, 0x2A, 0xEA, 0xEE,
            0x2E, 0x2F, 0xEF, 0x2D, 0xED, 0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26,
            0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60, 0x61, 0xA1, 0x63, 0xA3, 0xA2,
            0x62, 0x66, 0xA6, 0xA7, 0x67, 0xA5, 0x65, 0x64, 0xA4, 0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F,
            0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68, 0x78, 0xB8, 0xB9, 0x79, 0xBB,
            0x7B, 0x7A, 0xBA, 0xBE, 0x7E, 0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5,
            0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71, 0x70, 0xB0, 0x50, 0x90, 0x91,
            0x51, 0x93, 0x53, 0x52, 0x92, 0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C,
            0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B, 0x99, 0x59, 0x58, 0x98, 0x88,
            0x48, 0x49, 0x89, 0x4B, 0x8B, 0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,
            0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, 0x43, 0x83, 0x41, 0x81, 0x80,
            0x40
        ]

    @classmethod
    def calculateCrc16(cls, data):
        crcHigh, crcLow = 0xff, 0xff
        index = 0
        for byte in data:
            index = crcLow ^ byte
            crcLow  = crcHigh ^ cls.CRCTableHigh[index]
            crcHigh = cls.CRCTableLow[index]
        return (crcHigh << 8 | crcLow)

# class helper:
#     @classmethod
#     def calculateFrequency(cls):
#         return transmitPacket.pumpFreqMin \
#             + (transmitPacket.tempDesired - transmitPacket.tempDesiredMin) \
#             / (transmitPacket.tempDesiredMax - transmitPacket.tempDesiredMin) \
#             * (transmitPacket.pumpFreqMax - transmitPacket.pumpFreqMin)

class transmitPacket:
    command = 0 # default command
    tempSensor = 0
    tempDesired = 0
    pumpFreqMin = 0
    pumpFreqMax = 0
    funSpeedMin = 0
    funSpeedMax = 0
    voltageType = 0
    fanspeedSensor = 0
    thermostatMode = 0
    tempDesiredMin = 0
    tempDesiredMax = 0
    glowPlugPower = 0
    manualPump = 0
    altitude = 0

class heater:
    srl:Serial = None
    transmitPacket = transmitPacket
    runState = 0
    onOff = 0
    supplyVoltage = 0
    fanRpm = 0
    fanVoltage = 0
    heatExchTemp = 0
    glowPlugVoltage = 0
    glowPlugCurrent = 0
    actualPumpFreq = 0
    errorCode = 0
    fixedModePumpFreq = 0
    displayGradHzUnit = ""
    displayGradHzValue = 0
    #calculateFreq = helper.calculateFrequency()
    lastSend = time.time()

    @classmethod
    def createTransmitPacket(cls):
        try:
            transmitPacket.tempSensor = int(config.dieselHeater.tampSensor) # default or get temperature from BME280
            transmitPacket.tempDesired = int(config.dieselHeater.tempDesired)
            transmitPacket.pumpFreqMin = int(config.dieselHeater.pumpFreqMin * 10)
            transmitPacket.pumpFreqMax = int(config.dieselHeater.pumpFreqMax * 10)
            transmitPacket.funSpeedMin = int(config.dieselHeater.funSpeedMin)
            transmitPacket.funSpeedMax = int(config.dieselHeater.funSpeedMax)
            transmitPacket.voltageType = int(config.dieselHeater.voltageType * 10)
            transmitPacket.fanspeedSensor = int(config.dieselHeater.fanspeedSensor)
            transmitPacket.thermostatMode = int(config.dieselHeater.thermostatMode)
            transmitPacket.tempDesiredMin = int(config.dieselHeater.tempDesiredMin)
            transmitPacket.tempDesiredMax = int(config.dieselHeater.tempDesiredMax)
            transmitPacket.glowPlugPower = int(config.dieselHeater.glowPlugPower)
            transmitPacket.manualPump = int(config.dieselHeater.manualPump)
            transmitPacket.altitude = int(config.dieselHeater.altitude) # or get altitude from BME280

            buf = bytes([0] * 24)
            buf[0] = 0x76 # (118).to_bytes(1, byteorder='big') #Start of Frame - 0x76 for LCD
            buf[1] = 0x16 #(22).to_bytes(1, byteorder='big') #Data Size 24bytes
            buf[2] = transmitPacket.command.to_bytes(1, byteorder='big') #command
            # transmitPacket.command = 0 # reset command to 0x00
            # buf[3] = transmitPacket.tempSensor.to_bytes(1, byteorder='big') if transmitPacket.thermostatMode == 1 else 0 #temp sensor
            # buf[4] = transmitPacket.tempDesired.to_bytes(1, byteorder='big') #desired temp
            # buf[5] = transmitPacket.pumpFreqMin.to_bytes(1, byteorder='big') #Minimum Pump frequency
            # buf[6] = transmitPacket.pumpFreqMax.to_bytes(1, byteorder='big') #Maximum Pump frequency
            # buf[7] = transmitPacket.funSpeedMin.to_bytes(2, byteorder='big')[0] #Minimum fan speed MSB, LSB
            # buf[8] = transmitPacket.funSpeedMin.to_bytes(2, byteorder='big')[1]
            # buf[9] = transmitPacket.funSpeedMax.to_bytes(2, byteorder='big')[0] #Maximum fan speed MSB, LSB
            # buf[10] = transmitPacket.funSpeedMax.to_bytes(2, byteorder='big')[1]
            # buf[11] = transmitPacket.voltageType.to_bytes(1, byteorder='big')#Heater Operating Voltage 
            # buf[12] = transmitPacket.fanspeedSensor.to_bytes(1, byteorder='big') #Fan speed sensor
            # buf[13] = (50).to_bytes(1, byteorder='big') if transmitPacket.thermostatMode == 1 else (205).to_bytes(1, byteorder='big') #Thermostat/Fixed mode, buf[3] = 0 when fixed mode
            # buf[14] = transmitPacket.tempDesiredMin.to_bytes(1, byteorder='big') #Lower temperature limit
            # buf[15] = transmitPacket.tempDesiredMax.to_bytes(1, byteorder='big') #Upper temperature limit
            # buf[16] = transmitPacket.glowPlugPower.to_bytes(1, byteorder='big') #Glow Plug Power
            # buf[17] = transmitPacket.manualPump.to_bytes(1, byteorder='big') #Manual pump (fuel prime) 0x5A
            # buf[18] = (235).to_bytes(1, byteorder='big')
            # buf[19] = (71).to_bytes(1, byteorder='big') #unknown 0xEB MSB and 0x47 LSB for LCD controller
            # buf[20] = transmitPacket.altitude.to_bytes(2, byteorder='big')[0] #Altitude MSB, LSB
            # buf[21] = transmitPacket.altitude.to_bytes(2, byteorder='big')[1]

            #crc = modbusCRC.calculateCrc16(buf[0:21])
            #buf[22], buf[23] = crc & 0xFF, crc >> 8
        except Exception as e:
            logging.error(f"dieselHeater - createTransmitPacket - {e}")

        return buf
    
    @classmethod
    def translateReceivePacket(cls, buf):
        try:
            cls.runState = int.from_bytes(buf[2])
            cls.onOff = int.from_bytes(buf[3])
            cls.supplyVoltage = int.from_bytes(buf[4]) / 10
            cls.fanRpm = int.from_bytes(buf[6:7])
            cls.fanVoltage = int.from_bytes(buf[8:9]) / 10
            cls.heatExchTemp = int.from_bytes(buf[10:11])
            cls.glowPlugVoltage = int.from_bytes(buf[12:13]) / 10
            cls.glowPlugCurrent = int.from_bytes(buf[14:15]) / 100
            cls.actualPumpFreq = int.from_bytes(buf[16]) / 10
            cls.errorCode = int.from_bytes(buf[17])
            cls.fixedModePumpFreq = int.from_bytes(buf[19])

            cls.displayGradHzValue = transmitPacket.tempDesired if transmitPacket.thermostatMode == 1 else cls.actualPumpFreq
            cls.displayGradHzUnit = "°C".encode("latin-2","ignore") if transmitPacket.thermostatMode == 1 else "Hz"
        except Exception as e:
            logging.error(f"dieselHeater: {e}")

    @classmethod
    async def sendPacket(cls):
        try:
               
                # if cls.srl is None:
                #     dieselHeaterDevice = device.FindUsbDevice(config.dieselHeater.device)
                #     cls.srl = Serial(dieselHeaterDevice, 25000)

                # if cls.srl.closed:
                #     cls.srl.open()

                buf_transmit = heater.createTransmitPacket()
                logging.info(f"DieselHeater buf_transmit = {buf_transmit}")
                #cls.srl.write(buf_transmit)
                await asyncio.sleep(0.1)
                #buf_receive = cls.srl.read(48) # 48?
                #heater.translateReceivePacket(buf_receive[:24])
                cls.lastSend = time.time()

        except Exception as e:
            logging.error(f"dieselHeater: {e}")

        await asyncio.sleep(0.1)

    @classmethod
    async def sendPacketLoop(cls):
        while True:
            try:
                if time.time() - cls.lastSend < 2:
                    await asyncio.sleep(3)
                await cls.sendPacket()
                #await asyncio.sleep(interval)
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
    async def readData(cls, interval):
         await heater.sendPacketLoop()
    
class plugin:
   
    @classmethod
    async def initialize(cls, event_loop):
        event_loop.create_task(heater.sendPacketLoop())
