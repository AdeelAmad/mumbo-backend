from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.pain, name='user'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]