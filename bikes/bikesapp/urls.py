from django.urls import path
from . import views


urlpatterns = [
    path('', views.add_to_db, name="index"),
    path('<int:station_id>/', views.station_detail, name="station_detail"),
    # path('<int:question_id>/results/', views.results, name="results"),
    # path('<int:question_id>/vote/', views.vote, name="vote"),
]
