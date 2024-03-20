#------------------------
# pip install influxdb influxdb-client
# bash: influx
# CREATE DATABASE CamPanel
# exit
#------------------------
from influxdb import InfluxDBClient
import datetime
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from general.configLoader import config
from plugins import waterLevel, dalyBms, temperatures, epeverTracer
from general.logger import logging

class data:
    host = config.influxDB.host
    port = config.influxDB.port
    database = config.influxDB.database
    retentionData = config.influxDB.retentionData
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
    def deleteOldData(cls, bucket):
        try:
            cls.connectToInfluxDB()
            data.client.switch_database(data.database)
            query = f'DELETE FROM "{bucket}" WHERE time < now() - {data.retentionData}'
            data.client.query(query)
            data.client.close()
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
    async def logData(cls, measurement_name, tags, fields):
        jsonBody = [
            {
                "measurement": measurement_name,
                "tags": tags,
                "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": fields
            }
        ]
        cls.addToInfluxDB(jsonBody)         

    @classmethod
    async def logBmsData(cls, interval):
        while True:
            fields = {
                "totalVoltage": dalyBms.data.totalVoltage,
                "currentMiliAmper": dalyBms.data.currentMiliAmper,
                "RSOC": dalyBms.data.RSOC
            }            
            await cls.logData("BMS", {}, fields)
            await asyncio.sleep(interval)

    @classmethod
    async def logWaterLevelData(cls, interval):
        while True:
            fields = {
                "whiteWaterLevel": waterLevel.data.whiteWaterLevel,
                "grayWaterLevel": waterLevel.data.greyWaterLevel
            }
            
            await cls.logData("WaterLevel", {}, fields)
            await asyncio.sleep(interval)   

    @classmethod
    async def logEpeverTracerData(cls, interval):
        while True:
            fields = {
                "pvVoltage": epeverTracer.pv.voltage,
                "pvCurrent": epeverTracer.pv.current,
                "pvPower": epeverTracer.pv.power,
                "batVoltage": epeverTracer.battery.voltage,
                "batCurrent": epeverTracer.battery.current,
                "batSoc": epeverTracer.battery.soc,
                "batCapacity": epeverTracer.battery.capacity,
                "batTemperature": epeverTracer.battery.temp,
                "loadVoltage": epeverTracer.load.voltage,
                "loadCurrent": epeverTracer.load.current,
                "loadPower": epeverTracer.load.power
            }

            await cls.logData("EpeverTracer", {}, fields)
            await asyncio.sleep(interval)               

    @classmethod
    async def logTemperatureData(cls, interval):
        while True:
            fields = {
                "inTemp": temperatures.data.inTemp,
                "outTemp": temperatures.data.outTemp
            }

            await cls.logData("Temperature", {}, fields)
            await asyncio.sleep(interval)  

    @classmethod
    def logRelay(cls, relayIndex, value):
        fields = {
            f"relay{relayIndex}": value
        }    
                    
        cls.logData("Relays", {}, fields)

    @classmethod
    async def CutOldData(cls, interval):
        while True:
            cls.deleteOldData("BMS")
            cls.deleteOldData("WaterLevel")
            cls.deleteOldData("Temperature")
            cls.deleteOldData("Relays")
            cls.deleteOldData("EpeverTracer")
            await asyncio.sleep(interval)  

    @classmethod
    async def initialize(cls, event_loop):
        #cls.createDatabaseIfNotExists(cls)
        event_loop.create_task(cls.logBmsData(5))
        event_loop.create_task(cls.logTemperatureData(60))
        event_loop.create_task(cls.logWaterLevelData(60))
        event_loop.create_task(cls.logEpeverTracerData(5))
        event_loop.create_task(cls.CutOldData(1500))