from django.urls import path
from .views import calculate, consumer_list

urlpatterns = [
    path("calculator/", calculate),
    path("consumer/", consumer_list),
]
