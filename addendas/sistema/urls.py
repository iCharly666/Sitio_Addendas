from django.urls import path

from . import views


app_name = 'sistema'
urlpatterns = [
    path('', views.Inicio, name='inicio'),
    path('terra_multitransportes', views.Terra_Multi, name='terra'),
    path('open_lenguage', views.open_lenguge, name='lenguage'),


    
]