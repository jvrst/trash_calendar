from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from ics import Calendar, Event, DisplayAlarm
import requests
from datetime import timedelta, datetime

@dataclass
class Config(YAMLWizard):
    company_code: str
    address_id: str
    start_date: str
    end_date: str

    @property
    def api_parameters(self):
        return f"companyCode={self.company_code}&uniqueAddressID={self.address_id}&startDate={self.start_date}&endDate={self.end_date}"

def get_pickup_dates(config: Config):
    data = config.api_parameters
    url = "https://twentemilieuapi.ximmio.com/api/GetCalendar"
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    res = requests.post(url, headers=headers, data=data)
    return res.json()["dataList"]

def add_pickup_dates(dates, name, calendar: Calendar):
    for date in dates:
        e = Event()
        e.name = name
        e.begin = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S") + timedelta(hours=7)
        e.duration = timedelta(minutes=15)
        e.alarms.append(DisplayAlarm(trigger=timedelta(hours=-12)))
        calendar.events.add(e)

def get_name(type):
    type_text = type["_pickupTypeText"]
    friendly_text = ""
    if type_text == "GREEN":
        friendly_text = "Bio (groene) bak"
    elif type_text == "GREY":
        friendly_text = "Restafval (grijze) bak"
    elif type_text == "PACKAGES":
        friendly_text = "Plastic (oranje) bak"
    elif type_text == "PAPER":
        friendly_text = "Papier (blauwe) bak"
    elif type_text == "TREE":
        friendly_text = "Kerstboom"
    else:
        friendly_text = type_text
    return f"{friendly_text} aan straat"

def get_calendar(file_path: str | None = None) -> Calendar:
    if not file_path:
        return Calendar()
    with open(file_path, "r") as file:
        ics_text = file.read()
    return Calendar(ics_text)

def update_ics_file(calendar: Calendar, file: str):
    with open(file, "w") as ics_file:
        ics_file.writelines(calendar.serialize_iter())

if __name__ == "__main__":
    # config_file = yaml.safe_load(open("./config.yml"))
    config = Config.from_yaml_file("./config.yml")

    if isinstance(config, list):
        config = config[0]

    trash_types = get_pickup_dates(config)
    calendar = get_calendar()
    print(config)

    for type in trash_types:
        name = get_name(type)
        add_pickup_dates(type["pickupDates"], name, calendar)

    update_ics_file(calendar, f"trash-{datetime.now().replace(microsecond=0).isoformat()}.ics")
