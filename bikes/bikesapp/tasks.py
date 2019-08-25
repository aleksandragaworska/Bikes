from .models import Station, StationState
from .parse import get_data

from celery import task
import logging

logger = logging.getLogger(__name__)


@task()
def update_station_states():
    station_states, station_infos = get_data()

    for station_info in station_infos:
        station = Station()
        station.station_id = station_info[0]
        station.name = station_info[1]
        station.lat = station_info[2]
        station.lon = station_info[3]
        station.racks = station_info[4]
        station.save()
    logger.info(f'Saved station info for {len(station_infos)} stations')

    for station_state in station_states:
        state = StationState()
        state.station_id = station_state[0]
        state.date = station_state[2]
        state.bikes_count = station_state[1]
        state.save()
    logger.info(f'Saved station state for {len(station_states)} stations')
