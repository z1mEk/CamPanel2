#------------------------
# pip install influxdb influxdb-client
# bash: influx
# CREATE DATABASE CamPanel
# exit
#------------------------
from influxdb import InfluxDBClient
import datetime
import nest_asyncio
from general.configLoader import config
nest_asyncio.apply()
from plugins import waterLevel, dalyBms, temperatures
from general.logger import logging

class data:
    host = config.influxDB.host
    port = config.influxDB.port
    database = config.influxDB.database
    client = None
    
class plugin:

    @classmethod
    def connectToInfluxDB(cls):
        if data.client == None:
            try:
                data.client = InfluxDBClient(data.host, data.port)
            except Exception as e:
                logging.error(f"InfluxDb: {e}")

    @classmethod
    def createDatabaseIfNotExists(cls):
        try:
            cls.connectToInfluxDB()        
            databases = data.client.get_list_database()
            if {'name': data.client.database} not in databases:
                data.client.create_database(data.client.database)
        except Exception as e:
            logging.error(f"InfluxDb: {e}")

    @classmethod
    def addToInfluxDB(cls, jsonBody):
        try:
            cls.connectToInfluxDB()
            data.client.switch_database(data.database)
            data.client.write_points(jsonBody)
            data.client.close()       
        except Exception as e:
            logging.error(f"InfluxDb: {e}")

    @classmethod
    async def logBmsData(cls, interval):
        while True:
            jsonBody = [
                {
                    "measurement": "BMS",
                    "tags": {},
                    "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "fields": {
                        "totalVoltage": dalyBms.data.totalVoltage,
                        "currentMiliAmper": dalyBms.data.currentMiliAmper,
                        "RSOC": dalyBms.data.RSOC
                    }
                }
            ]
            cls.addToInfluxDB(jsonBody)
            await nest_asyncio.asyncio.sleep(interval)

    @classmethod
    async def logWaterLevelData(cls, interval):
        while True:
            jsonBody = [
                {
                    "measurement": "WaterLevel",
                    "tags": {},
                    "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "fields": {
                        "whiteWaterLevel": waterLevel.data.whiteWaterLevel,
                        "grayWaterLevel": waterLevel.data.greyWaterLevel
                    }
                }
            ]
            cls.addToInfluxDB(jsonBody)
            await nest_asyncio.asyncio.sleep(interval)   

    @classmethod
    async def logTemperatureData(cls, interval):
        while True:
            jsonBody = [
                {
                    "measurement": "Temperature",
                    "tags": {},
                    "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "fields": {
                        "temp1": temperatures.data.temp1,
                        "temp2": temperatures.data.temp2
                    }
                }
            ]
            cls.addToInfluxDB(jsonBody)
            await nest_asyncio.asyncio.sleep(interval)  

    @classmethod
    def logRelay(cls, relayIndex, value):
        jsonBody = [
            {
                "measurement": "Relays",
                "tags": {},
                "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                    f"relay{relayIndex}": value
                }                
            }
        ]
        cls.addToInfluxDB(jsonBody)

    @classmethod
    async def initialize(cls, event_loop):
        #cls.createDatabaseIfNotExists(cls)
        event_loop.create_task(cls.logBmsData(5))
        event_loop.create_task(cls.logTemperatureData(60))
        event_loop.create_task(cls.logWaterLevelData(60))