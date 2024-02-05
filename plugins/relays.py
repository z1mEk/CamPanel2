import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from enum import Enum
from general.configLoader import config
from general.deviceManager import device
from serial import Serial
from plugins import influxDBLog
from datetime import datetime
from general.logger import logging
from plugins.hmi import methods as methodsHmi

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
    
class RelayAddress(Enum):
    RELAY0 = (1,0)
    RELAY1 = (1,1)
    RELAY2 = (1,2)
    RELAY3 = (1,3)
    RELAY4 = (1,4)
    RELAY5 = (1,5)
    RELAY6 = (1,6)
    RELAY7 = (1,7)

class relayMeta(type):
    address = None

    @property
    def val(self):
        return self.getRelayState()
        
    @val.setter
    def val(self, value):
        self.setRelayState(value)

class relayMethod(metaclass=relayMeta):

    @classmethod
    def toggle(cls):
        cls.val = 1 if cls.val == 0 else 0

    @classmethod
    def on(cls):
        cls.val = 1

    @classmethod
    def off(cls):
        cls.val = 0
    
    @classmethod
    def setRelayState(cls, value:int):
        cmd = [0] * 8
        cmd[0] = cls.address.value[0]
        cmd[1] = 0x05
        cmd[3] = cls.address.value[1]
        cmd[4] = value if (value == 0) else 0xFF
        crc = modbusCRC.calculateCrc16(cmd[0:6])
        cmd[6], cmd[7] = crc & 0xFF, crc >> 8
        try:
            relays_device = device.FindUsbDevice(config.relays.device)
            srl = Serial(relays_device, config.relays.baudrate)
            srl.write(cmd)
            srl.close()
            data.relaysState[cls.address.value[1]] = value
            cls.onRelayChange(cls.address.value[1], value)
        except Exception as e:
            logging.error(f"Relays set: {e}")

    @classmethod
    def getRelaysState(cls):
        cmd = [0] * 8
        cmd[0] = 0x00
        cmd[1] = 0x01
        cmd[3] = 0xff
        cmd[5] = 0x01
        crc = modbusCRC.calculateCrc16(cmd[0:6])
        cmd[6], cmd[7] = crc & 0xFF, crc >> 8
        try:
            relays_device = device.FindUsbDevice(config.relays.device)
            srl = Serial(relays_device, config.relays.baudrate)
            srl.write(cmd)
            buffer = srl.read(6)
            srl.close()
            data.relaysState = [int(bit) for bit in f'{buffer[3]:08b}'][::-1]
            data.lastUpdate = datetime.now() 
        except Exception as e:
            logging.error(f"Relays get: {e}")       

    @classmethod
    def getRelayState(cls) -> int:
        if data.relaysState == None:
            cls.getRelaysState()
        return data.relaysState[cls.address.value[1]]
    
    @classmethod
    def onRelayChange(cls, relayIndex, value):
        influxDBLog.plugin.logRelay(relayIndex, value)
        logging.debug(f"onRelayChange({relayIndex}, {value})")
        
class TRelay(relayMethod):
    pass

class data:

    relaysState = None
    lastUpdate = None
 
    class relay0(TRelay):
        address = RelayAddress.RELAY0

        @classmethod
        def onRelayChange(cls, relayIndex, value):
            return super().onRelayChange(relayIndex, value)

    class relay1(TRelay):
        address = RelayAddress.RELAY1

        @classmethod
        def onRelayChange(cls, relayIndex, value):
            return super().onRelayChange(relayIndex, value)

    class relay2(TRelay):
        address = RelayAddress.RELAY2

        @classmethod
        def onRelayChange(cls, relayIndex, value):
            return super().onRelayChange(relayIndex, value)

    class relay3(TRelay):
        address = RelayAddress.RELAY3

        @classmethod
        def onRelayChange(cls, relayIndex, value):
            return super().onRelayChange(relayIndex, value)        

    class relay4(TRelay):
        address = RelayAddress.RELAY4

        @classmethod
        def onRelayChange(cls, relayIndex, value):
            return super().onRelayChange(relayIndex, value)        

    class relay5(TRelay):
        address = RelayAddress.RELAY5

        @classmethod
        def onRelayChange(cls, relayIndex, value):
            return super().onRelayChange(relayIndex, value)        

    class relay6(TRelay):
        address = RelayAddress.RELAY6

        @classmethod
        def onRelayChange(cls, relayIndex, value):
            return super().onRelayChange(relayIndex, value)        

    class relay7(TRelay):
        address = RelayAddress.RELAY7

        @classmethod
        def onRelayChange(cls, relayIndex, value):
            return super().onRelayChange(relayIndex, value)        

    relays = [relay0, relay1, relay2, relay3, relay4, relay5, relay6, relay7]

class plugin:

    @classmethod
    async def readData(cls, interval):
        relayMethod.getRelaysState()

    @classmethod
    async def initialize(cls, event_loop): 
        event_loop.create_task(cls.readData(1))
