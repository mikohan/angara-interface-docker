from .views import ProductDoneView
from django.urls import path

urlpatterns = [
    path("", ProductDoneView.as_view()),
]
