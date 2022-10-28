from django.urls import path, include
from test_category.api import views, vehicle_views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"testproducts", views.SingleProductView)
router.register(r"vehicles", vehicle_views.VehicleView)


urlpatterns = [
    path("testproducts/", include(router.urls)),
    # Url for getting flat categories with one level of parent
    path("testcategories/", views.CategoriesView.as_view(), name="cat-test"),
    path(
        "categories-for-testes/",
        views.CategoriesViewForTestes.as_view(),
        name="cat-testes",
    ),
    # get category by slug for red parts categories
    # url is http://localhost:8000/testcategory/category/dvigatel/
    path(
        "testcategory/<slug:slug>/",
        views.SingleCategorySlugView.as_view(),
        name="cat-test-slug",
    ),
    path(
        "testyears/",
        vehicle_views.YearsView.as_view(),
        name="years",
    ),
    path(
        "testmodels/<str:make>/",
        vehicle_views.VehiclesBySlugView.as_view(),
        name="vehicle-by-slug",
    ),
    path("testmakes/", vehicle_views.MakesView.as_view(), name="makes-all"),
    path(
        "recursivecategories/",
        views.CategoriesViewRecursive.as_view(),
        name="recursive-views",
    ),
]
