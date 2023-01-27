# Goodwe data scraper
Scrape the Goodwe inverter data and write to InfluxDB or a file
</br>

![01](https://user-images.githubusercontent.com/43645090/195945343-cbf43ec1-dfd5-46f4-84d1-1fb0b7f8eb95.png)
![02](https://user-images.githubusercontent.com/43645090/195945355-ea10296e-d2f5-4421-a543-a858fd01f8b6.png)

tested on models: 
GoodWe GW10K-ET
GoodWe GW3648D-ES
</br>


## Installation

1. install `goodwe` and `influxdb-client` modules for python:
```
python -m pip install goodwe
python -m pip install influxdb_client
```

2. create a monitoring stack with deployment/docker-compose.yml file (this will install influxdb and grafana in docker):</br>
  2.1 edit following files before running docker-compose:</br> 
    - deployment/config.env - change create your own usernames, passwords and bucket name </br>
    - deployment/grafana/provisioning/datasources/datasource.yml</br>
  2.2 run:</br>
```
        cd deployment
        docker-compose up -d
```

</br>

3. Create an influxdb bucket and insert the influxdb URL, bucketname, org and token into config.py
   to create the API token, follow the instruction on the InfluxDB website: https://docs.influxdata.com/influxdb/v2.4/security/tokens/create-token/

4. after you created the bucket and API token in influxDB, insert them into `config.py` and `deployment/grafana/provisioning/datasources/datasource.yml` and run `docker-compose up -d` again to update the datasource setup in grafana

5. go to Grafana -> settings -> datasources -> InfluxDB -> and klick on "Test", to check if the Datasource is working correctly

6. Run the scraper manually with:
```
python goodwe_get_data.py
```
and check if you got data in influxDB and grafana

</br>

7. if everything is OK, create a cronjob to get every 5 min the data

```
*/5 * * * * <username> python /<absolute_path_to_script>/goodwe_get_data.py
```

</br>


## Configurations
`config.py` file explanation:</br>
</br>
| Value:| |
| :--- | :--- |
|**ENERGY_PRICE**| price in eur per kWh - user for correct counting in grafana dashboard|
|**SCRAPE_ALL_METRICS**| if set to 'True', all metrics will be scraped. otherwise metrics from `CUSTOM_MEASUREMENTS` list are scraped|
|**CUSTOM_MEASUREMENTS**| if you do not wish to scrape all metrics, you can set, which metrics to scrape. A complete list can be found in file 'measurements-list.txt'|
|**HEALTHCHECK_ENABLED**| enable/disable monitoring via Healthchecks.io|
|**HEALTHCHECK_UID**| your UID on Healthchecks.io|
|**INVERTER_IP**| IP adress of your Goodwe inverter|
|**INFLUXDB_WRITE_ENABLED**| if True, scraped data is written into InfluxDB|
|**INFLUXDB_URL**| URL of your InfluxDB|
|**INFLUXDB_TOKEN**| InfluxDB token - must have write permission in influx|
|**INFLUXDB_ORG**| organisation|
|**INFLUXDB_BUCKET**| InfluxDB bucket in which the scraped data should be stored|
