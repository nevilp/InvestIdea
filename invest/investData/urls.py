from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^data', views.getData,name='getdata'),
    path('', views.index, name='index'),

]