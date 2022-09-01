import asyncio
import goodwe
from datetime import date

#Config
ip_address = '192.168.2.35' #Add here the IP adress of the inverter
logfilePath = "/data/goodwe-data-scraper"


current_date = str(date.today())

async def get_runtime_data():
    inverter = await goodwe.connect(ip_address)
    runtime_data = await inverter.read_runtime_data()

    with open(logfilePath+'/data-'+current_date+'.txt', 'w') as f:
        for sensor in inverter.sensors():
            if sensor.id_ in runtime_data:
                #print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")
                f.write(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}\n")


asyncio.run(get_runtime_data())
