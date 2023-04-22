from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('for-clients/', views.for_clients, name='clients'),
    path('for-attorneys/', views.for_attorneys, name='attorneys'),
    path('contact/', views.contact, name='contact'),
]
