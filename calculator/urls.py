from django.urls import path
from .views import (
  calculator,
  consumer_list,
  consumer_create,
  home
)

urlpatterns = [
    path("", home),
    path("calculator/", calculator),
    path("consumer/", consumer_list),
    path("consumer/create", consumer_create),
]
