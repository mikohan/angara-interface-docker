from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import datetime, time
from django.conf import settings

from product.models import Product


class ProductDoneView(ListView, LoginRequiredMixin):
    model = Product
    queryset = Product.objects.all()
    template_name = "stats/index.html"
    context_object_name = "objects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["frontend_url"] = settings.FRONTEND_URL
        return context

    def get_queryset(self):
        request = self.request
        start = request.GET.get("start", str(datetime.date.today()))
        end = request.GET.get("end", str(datetime.date.today()))
        qs = self.queryset

        if start == end:
            print("im here")
            qs = self.queryset.filter(
                updated_date__gte=start, updated_date__lt=f"{end} 23:59:59"
            )[:400]
        elif start and end:
            qs = self.queryset.filter(updated_date__range=(start, end))[:400]
        elif start and not end:
            qs = self.queryset.filter(
                updated_date__gte=start, updated_date__lt=f"{start} 23:59:59"
            )[:400]
        elif not start and end:
            qs = self.queryset.filter(
                updated_date__gte=end, updated_date__lt=f"{end} 23:59:59"
            )[:400]

        return qs
