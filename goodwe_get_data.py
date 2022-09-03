import asyncio
import goodwe
import os
import secrets
import time
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# get current directory of this script
CURRENT_DIR=(os.path.dirname(os.path.realpath(__file__)))


# Configure InfluxDB connection variables
_client = InfluxDBClient(url=secrets.INFLUXDB_URL, token=secrets.INFLUXDB_TOKEN, org=secrets.INFLUXDB_ORG)
_write_api = _client.write_api(write_options=SYNCHRONOUS)

try:
    async def get_runtime_data():
        inverter = await goodwe.connect(secrets.INVERTER_IP)
        runtime_data = await inverter.read_runtime_data()
    
        f=open(CURRENT_DIR+"/data-"+time.strftime("%Y-%m-%d")+'.txt', "w+")
        for sensor in inverter.sensors():
            if sensor.id_ in runtime_data:
                #write to file
                f.write(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}\n")

                #write here the condition for specific values to add to DB - !!! never add "timestamp" !!!
                #measurements = ('e_total', 'e_day', 'e_total_exp', 'h_total', 'e_day_exp', 'e_total_imp', 'e_day_imp', 'e_load_total', 'e_load_day')
                #if sensor.id_ in measurements:

                if sensor.id_ != "timestamp":
                    point = Point(sensor.name) \
                          .tag("type", "FVE") \
                          .field(sensor.id_, runtime_data[sensor.id_]) \
                          .time(datetime.utcnow(), WritePrecision.NS)

                    _write_api.write(secrets.INFLUXDB_BUCKET, secrets.INFLUXDB_ORG, point)
        f.close()

    asyncio.run(get_runtime_data())

except KeyboardInterrupt:
    _write_client.__del__()
    _client.__del__()
    pass
