import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import pytz


def get_data():
    response = requests.get('https://nextbike.net/maps/nextbike-live.xml?city=210')

    root = ET.fromstring(response.content)
    timezone = pytz.timezone("Europe/Warsaw")
    now = datetime.now()
    local_time = timezone.localize(now)
    station_state = []
    station_info = set()
    for child in root.iter('place'):
        station_state.append([child.attrib['number'], child.attrib['bikes'], local_time])
        station_info.add((child.attrib['number'], child.attrib['name'], child.attrib['lat'], child.attrib['lng'], child.attrib['bike_racks']))

    # print(station_state)
    return station_state, station_info

# print()
# print(station_info)
