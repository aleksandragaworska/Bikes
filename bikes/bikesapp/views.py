from django.shortcuts import render
from django.http import HttpResponse
from .parse import get_data
from .models import Station, StationState


def add_to_db(request):
    station_states, station_infos = get_data()

    for station_info in station_infos:
        station = Station()
        station.station_id = station_info[0]
        station.name = station_info[1]
        station.lat = station_info[2]
        station.lon = station_info[3]
        station.racks = station_info[4]
        station.save()

    for station_state in station_states:
        state = StationState()
        state.station_id = station_state[0]
        state.date = station_state[2]
        state.bikes_count = station_state[1]
        state.save()

    return HttpResponse('Added!')
