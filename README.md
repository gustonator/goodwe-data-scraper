# Goodwe data scraper
Scrape the Goodwe inverter data and write to InfluxDB or a file
</br>

![grafana-screenshot](https://user-images.githubusercontent.com/43645090/188503114-e9c2d6cc-6237-4668-a308-5df757a87d2c.png)


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



