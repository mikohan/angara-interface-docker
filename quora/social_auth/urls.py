from .views import GoogleAuthView
from django.urls import path

urlpatterns = [
    path("google/", GoogleAuthView.as_view()),
]
