from django.urls import path

from . import views

app_name = 'configSalle'
urlpatterns = [
    path('', views.index, name='index'),
    # path('json/confs.json', views.loadjson, name='loadjson'),     # solution avortée du Json
]
