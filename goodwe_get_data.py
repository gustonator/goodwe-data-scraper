import asyncio
import goodwe
import os
import config
import time
import socket
import urllib.request
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# get current directory of this script
CURRENT_DIR=(os.path.dirname(os.path.realpath(__file__)))

# get current datetime
CURRENT_TIME = datetime.utcnow()

# Configure InfluxDB connection variables
_client = InfluxDBClient(url=config.INFLUXDB_URL, token=config.INFLUXDB_TOKEN, org=config.INFLUXDB_ORG)
_write_api = _client.write_api(write_options=SYNCHRONOUS)

try:
    async def get_runtime_data():
        inverter = await goodwe.connect(config.INVERTER_IP)
        runtime_data = await inverter.read_runtime_data()
    
        f=open(CURRENT_DIR+"/logs/data-"+time.strftime("%Y-%m-%d")+'.txt', "w+")
        for sensor in inverter.sensors():
            if sensor.id_ in runtime_data:
                f.write(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}\n")

                # check if all metrics should be scraped or not
                if config.SCRAPE_ALL_METRICS:
                    measurements = sensor.id_
                else:
                    measurements = config.CUSTOM_MEASUREMENTS

                if sensor.id_ in measurements and sensor.id_ != "timestamp":
                    point = Point(sensor.name) \
                          .tag("type", "FVE") \
                          .field(sensor.id_, runtime_data[sensor.id_]) \
                          .time(CURRENT_TIME, WritePrecision.NS)

                    if config.INFLUXDB_WRITE_ENABLED:
                        _write_api.write(config.INFLUXDB_BUCKET, config.INFLUXDB_ORG, point)
        

        #Write energy price into influxDB
        point = Point("Energy price per kWh") \
                .tag("type", "FVE") \
                .field("energy_price", config.ENERGY_PRICE) \
                .time(CURRENT_TIME, WritePrecision.NS)

        if config.INFLUXDB_WRITE_ENABLED:
            _write_api.write(config.INFLUXDB_BUCKET, config.INFLUXDB_ORG, point)
        
        # write energy price to file
        f.write(f"energy_price: \t\t Energy price per kWh = {config.ENERGY_PRICE} eur\n")

        f.close()

    asyncio.run(get_runtime_data())

    
    # send notification to Healthchecks.io
    if config.HEALTHCHECK_ENABLED:
        urllib.request.urlopen("https://hc-ping.com/"+config.HEALTHCHECK_UID, timeout=10)

except KeyboardInterrupt:
    _write_client.__del__()
    _client.__del__()
    pass

