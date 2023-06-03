from django.urls import path, include

from . import views

urlpatterns = [
    path('birthday/', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
]
