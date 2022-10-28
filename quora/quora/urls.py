from django.contrib import admin
from django.urls import path, include, re_path

from django_registration.backends.one_step.views import RegistrationView
from django.conf import settings
from django.conf.urls.static import static

from users.forms import CustomUserForm
from core.views import IndexTemplateView
from django.views.generic import TemplateView
from home.views import Home, DocumentationView, React
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from test_category.views import elastic_file_create

schema_view = get_schema_view(
    openapi.Info(
        title="A77 API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


admin.site.site_header = "Мега Интерфейс"
admin.site.site_title = "Интерфейс"


urlpatterns = [
    path("yandex-market/", include("yandex_market.urls"), name="yandex-market"),
    path("elastic-file-create/", elastic_file_create, name="elastic-create"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("", Home.as_view(), name="home"),
    path("documentation/", DocumentationView.as_view(), name="documentation"),
    path("admin/", admin.site.urls),
    path(
        "accounts/register/",
        RegistrationView.as_view(
            form_class=CustomUserForm,
            success_url="/",
        ),
        name="django_r",
    ),
    path("stats/", include("stats.urls")),
    path("orders/", include("orders.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("django_registration.backends.one_step.urls")),
    path("product/", include("product.urls"), name="product-main"),
    path("api/brands/", include("brands.api.urls")),
    path("api/user/", include("users.api.urls")),
    path("api/product/", include("product.api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    # path("api/rest-auth/", include("rest_auth.urls")),
    # path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
    path("branddict/", include("brand_dict.urls")),
    path("blog/", include("blog.urls")),
    path("vasyainterface/", include("vasya_interface.urls")),
    path("companypages/", include("company_pages.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("auth/", include("authentication.urls")),
    path("auth/social/", include("social_auth.urls")),
    path(
        "authentication/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    # path("testcategory/", include("test_category.urls")),
    path("react/", React.as_view(), name="react"),
    re_path(r"^(?:react.*)/$", React.as_view(), name="react-router"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += [re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")]
