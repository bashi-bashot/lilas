from django.urls import path

from . import views

app_name = 'loadFic'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload_is_valid', views.uploadValid, name='uploadValid'),
]