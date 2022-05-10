from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('commands/', views.commands, name='commands'),
    path('privacy/', views.privacy, name='privacy'),
    path('tos/', views.tos, name='tos'),
    path('changelog/', views.changelog, name='changelog'),
    path('migration/', views.migration, name='migration'),
    path('invite/', views.invite, name='invite'),
]