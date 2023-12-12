from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [    
              

   path('', views.index, name='app'),
   path('excel/', views.excel, name='excel'), 
   path('CSV/', views.csv, name='csv'),
   path('text/', views.text, name='text'),
   path('url/', views.url, name='url'),
   path('visualiser/', views.visualiser, name='visualiser'),
   path('visualiserChart/', views.visualiser_chart, name='visualiser_chart'),
   path('diagramme/', views.diagramme, name='diagramme'),
   path('parcourir/', views.parcourir_chart, name='parcourir_chart'),
   path('binomiale/', views.Binomiale, name='Binomiale'),
   path('bernoulli/', views.Bernoulli, name='Bernoulli'),
   
]