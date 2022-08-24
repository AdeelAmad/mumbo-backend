from django.urls import path

from . import views

urlpatterns = [
    path('birthday/', views.index, name='index'),
]
