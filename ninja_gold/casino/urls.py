from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('games', views.index),
    path('games/farm', views.farm),
    path('games/cave', views.cave),
    path('games/house', views.house),
    path('games/casino', views.casino),
    path('games/reset', views.reset),
    #path('games/process_money', views.process_money),
]