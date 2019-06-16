from django.db import models


class Station(models.Model):
    station_id = models.IntegerField()
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    racks = models.IntegerField()


class StationState(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    date = models.DateTimeField()
    bikes_count = models.IntegerField()
