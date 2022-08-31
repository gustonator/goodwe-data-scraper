# Goodwe data scraper
Scrape the Goodwe inverter data and write to a file
</br></br>

[optional] upgrade pip to nevest version with `python -m pip install --upgrade pip`

install goodwe module: 
```
python -m pip install goodwe
```

</br>
create a cronjob to get every day before midnight the data (at 23:50)
```
50 23 * * * <username> python /<absolute_path_to_script>/goodwe_get_data.py
```

</br>

### TO-DO
- check if a file was created and if not, re-run the script - in case of power of network outage
- filter for specific items
