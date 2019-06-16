import requests
import xml.etree.ElementTree as ET
from datetime import datetime


response = requests.get('https://nextbike.net/maps/nextbike-live.xml?city=210')

root = ET.fromstring(response.content)

station_state = []
station_info = set()
for child in root.iter('place'):
    station_state.append([child.attrib['number'], child.attrib['bikes'], str(datetime.now())])
    station_info.add((child.attrib['number'], child.attrib['name'], child.attrib['lat'], child.attrib['lng'], child.attrib['bike_racks']))

print(station_state)
print()
print(station_info)
