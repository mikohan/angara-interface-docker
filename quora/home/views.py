from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from home.models import Documentation
from product.models import CarModel, CarMake, Product
from django.db.models import Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginRequiredMixin, TemplateView):
    """
    This class will aggregate all statistic by model
    To show in main analytics page on dashboard

    .annotate(attribute_count=Count('model_product', filter=Q(model_product__product_attribute__isnull=False), distinct=True)).annotate(video_count=Count('model_product', filter=Q(model_product__product_video__isnull=False), distinct=True)).annotate(related_count=Count('model_product', filter=Q(model_product__related__isnull=False), distinct=True))
    """

    template_name = "home/home_v2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        models = (
            CarModel.objects.all()
            .annotate(product_all_count=Count("model_product"))
            .annotate(
                photo_count=Count(
                    "model_product",
                    filter=Q(model_product__product_image__isnull=False),
                    distinct=True,
                )
            )
            .annotate(
                video_count=Count(
                    "model_product",
                    filter=Q(model_product__product_video__isnull=False),
                    distinct=True,
                )
            )
            .order_by("-product_all_count")
        )
        total_products = Product.objects.all()
        context["total_products"] = total_products.count()
        context["total_no_photo"] = total_products.filter(
            product_image__isnull=True
        ).count()
        context["models"] = models

        return context


class DocumentationView(TemplateView):
    template_name = "home/documentation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        some_data = Documentation.objects.all()
        context.update({"documentation": some_data})
        return context


class React(TemplateView):
    template_name = "home/react.html"
