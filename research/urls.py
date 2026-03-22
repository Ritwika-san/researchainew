from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('', views.home, name='home'),
    path('research/', views.research, name='research'),
]
