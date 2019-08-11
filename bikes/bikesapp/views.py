from django.shortcuts import render
from django.http import HttpResponse
from .parse import get_data
from .models import Station, StationState
import pytz


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


def station_detail(request, station_id):
    info = Station.objects.get(station_id=station_id)
    state = StationState.objects.filter(station_id=station_id).order_by('-date')[0]

    date_time_UTC = state.date
    timezone = pytz.timezone("Europe/Warsaw")
    date_time = date_time_UTC.astimezone(timezone)
    time = date_time.strftime('%H:%M:%S')
    day = date_time.strftime('%d.%m.%Y')
    weekday = date_time.strftime('%A')
    to_polish = {'Monday': 'poniedziałek',
                 'Tuesday': 'wtorek',
                 'Wednesday': 'środa',
                 'Thursday': 'czwartek',
                 'Friday': 'piątek',
                 'Saturday': 'sobota',
                 'Sunday': 'niedziela'}

    return HttpResponse(
        f'''
        Stacja {info.name} o numerze {info.station_id}
        posiada stojaki w liczbie {info.racks}.
        <br><br>
        O godzinie {time} dnia {day} ({to_polish[weekday]}) liczba wolnych
        rowerów do wypożyczenia wynosi {state.bikes_count}.
        '''
    )
