from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [    
               path('image/', views.image, name='image'),

   path('', views.index, name='app'),
   path('excel/', views.excel, name='excel'), 
   path('CSV/', views.csv, name='csv'),
   path('text/', views.text, name='text'),
   path('url/', views.url, name='url'),
   path('visualiser/', views.visualiser, name='visualiser')
   # path('upload-file/', views.upload_file, name='upload_file'),

   
]