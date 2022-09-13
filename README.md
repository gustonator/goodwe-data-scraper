# Goodwe data scraper
Scrape the Goodwe inverter data and write to InfluxDB or a file
</br>

![grafana_FVE_dashboard](https://user-images.githubusercontent.com/43645090/190007343-b923dfd6-b0fd-4e75-aa6b-bb597f252cf2.png)



## Installation

1. install `goodwe` and `influxdb-client` modules for python:
```
python -m pip install goodwe
python -m pip install influxdb_client
```

2. create a monitoring stack with deployment/docker-compose.yml file (this will install influxdb and grafana in docker)</br>
  2.1 edit following files before running docker-compose:</br> 
    - deployment/config.env</br>
    - deployment/grafana/provisioning/datasources/datasource.yml</br>
  2.2 run:</br>
```
        cd deployment
        docker-compose up -d
```

3. install and configure sun and moon plugin to grafana
   https://grafana.com/grafana/plugins/fetzerch-sunandmoon-datasource/
   https://github.com/fetzerch/grafana-sunandmoon-datasource

</br>

4. Create an influxdb bucket and insert the influxdb URL, bucketname, org and token into config.py

5. clone repo and run the scraper with:
```
python goodwe_get_data.py
```
</br>

6. if everything is OK, create a cronjob to get every 5 min the data

```
*/5 * * * * <username> python /<absolute_path_to_script>/goodwe_get_data.py
```

</br>


## Configurations
`config.py` file explanation:</br>
</br>
*ENERGY_PRICE* 		- price in eur per kWh - user for correct counting in grafana dashboard</br>
*SCRAPE_ALL_METRICS*	- if set to 'True', all metrics will be scraped. otherwise metrics from `CUSTOM_MEASUREMENTS` list are scraped</br>
*CUSTOM_MEASUREMENTS* 	- if you do not wish to scrape all metrics, you can set, which metrics to scrape. A complete list can be found in file 'measurements-list.txt'</br>

*HEALTHCHECK_ENABLED*	- enable/disable monitoring via Healthchecks.io</br>
*HEALTHCHECK_UID*	- your UID on Healthchecks.io</br>

*INVERTER_IP*		- IP adress of your Goodwe inverter</br>

*INFLUXDB_WRITE_ENABLED*- if True, scraped data is written into InfluxDB</br>
*INFLUXDB_URL*		- URL of your InfluxDB</br>
*INFLUXDB_TOKEN*	- InfluxDB token - must have write permission in influx</br>
*INFLUXDB_ORG*		- organisation</br>
*INFLUXDB_BUCKET*	- InfluxDB bucket in which the scraped data should be stored</br>
