# Trash calendar
Simple script to take the trash pickup dates and put them in an ICS file to be imported by a calendar app.
Solves the issue that I'd otherwise have to download yet another stupid app.

Used in Enschede, NL. 

If your trash pickup company is using Ximmio, you can use this script.
Copy the example config, fill in the fields (go to the trash calendar, check in devtools what your address and company IDs are. Daterange does not matter too much.

# How to run:
First make sure to setup a valid config.

```sh
cp config.yml.example config.yml
```

Then simply run the following:
```sh
poetry run python3 main.py
```

# Links:
https://www.twentemilieu.nl/enschede/afval/afvalkalender
https://twentemilieuapi.ximmio.com/api/GetCalendar
