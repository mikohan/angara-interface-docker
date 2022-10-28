from django.urls import path
from . import views


urlpatterns = [path("stocks", views.GetStock.as_view(), name="yandex-stocks")]
