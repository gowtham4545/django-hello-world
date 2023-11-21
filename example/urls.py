# example/urls.py
from django.urls import path

from example.views import *


urlpatterns = [
    path('', index),
    path('generate',generate),
    path('mail',mailto),
    path('keys',keys),
]