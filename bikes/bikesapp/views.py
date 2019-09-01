from django.shortcuts import render
from django.http import HttpResponse
from .parse import get_data
from .models import Station, StationState
import pytz
import logging

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

logger = logging.getLogger(__name__)


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
    logger.info(f'Saved station info for {len(station_infos)} stations')

    for station_state in station_states:
        state = StationState()
        state.station_id = station_state[0]
        state.date = station_state[2]
        state.bikes_count = station_state[1]
        state.save()
    logger.info(f'Saved station state for {len(station_states)} stations')

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


def stations_list(request):
    station_infos = Station.objects.all()
    context = {'stations_list': station_infos}
    return render(request, 'bikesapp/stations_list.html', context)
