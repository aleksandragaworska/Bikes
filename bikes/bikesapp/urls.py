from django.urls import path
from . import views


urlpatterns = [
    path('', views.add_to_db, name="index"),
    path('<int:station_id>/', views.station_detail, name="station_detail"),
    path('list/', views.stations_list, name="stations_list"),
    # path('<int:question_id>/vote/', views.vote, name="vote"),
]
