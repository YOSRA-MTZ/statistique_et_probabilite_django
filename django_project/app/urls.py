from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
   path('', views.index, name='app'),
   path('excel/', views.excel, name='excel'), 
   path('CSV/', views.csv, name='csv'),
   path('text/', views.text, name='text'),
   path('url/', views.url, name='url'),
]