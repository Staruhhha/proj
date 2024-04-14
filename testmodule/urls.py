from django.urls import path
from .views import *

urlpatterns = [
    path('date/', test_method, name='date_time')
]