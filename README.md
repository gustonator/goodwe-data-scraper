# Goodwe data scraper
Scrape the Goodwe inverter data and write to InfluxDB or a file 
</br></br>


install goodwe module: 
```
python -m pip install goodwe
```

install influxDB module:
```
python -m pip install influxdb_client
```

</br>
create a cronjob to get every 1 min the data

```
*/1 * * * * <username> python /<absolute_path_to_script>/goodwe_get_data.py
```

</br>

