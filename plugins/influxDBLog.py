#------------------------
# pip3 install inluxdb
# bash: influx
# CREATE DATABASE moja_baza_danych
# exit
#------------------------
from influxdb import InfluxDBClient
import datetime
import nest_asyncio
from general.config_loader import config
nest_asyncio.apply()

class data:
    host = config.influxDB.host
    port = config.influxDB.port
    database = config.influxDB.database
    client = None
    
class plugin:

    @classmethod
    async def connectToInfluxDB(cls):
        data.client = InfluxDBClient(data.host, data.port)

    @classmethod
    async def createDatabaseIfNotExists(cls):
        if data.client == None:
            await cls.connectToInfluxDB()        
        databases = data.client.get_list_database()
        if {'name': data.client.database} not in databases:
            data.client.create_database(data.client.database)    

    @classmethod
    async def saveToInfluxDB(cls, jsonBody):
        if data.client == None:
            await cls.connectToInfluxDB()
            data.client.switch_database(data.database)
            data.client.write_points(jsonBody)
            data.client.close()            

    @classmethod
    async def logBmsData(cls, interval):
        while True:
            jsonBody = [
                {
                    "measurement": "BMS",
                    "tags": {},
                    "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "fields": {
                        "variable1": 1,
                        "variable2": 2
                    }
                }
            ]
            await cls.saveToInfluxDB(jsonBody)
            await nest_asyncio.asyncio.sleep(interval)       

    @classmethod
    async def initialize(cls, event_loop):
        await cls.createDatabaseIfNotExists()
        event_loop.create_task(cls.logBmsData(5))