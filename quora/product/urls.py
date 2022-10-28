from django.urls import path, include, re_path
from product import views as productviews
from graphene_django.views import GraphQLView
from product.schema import schema
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # path('', TemplateView.as_view(template_name='index1.html')),
    path("", productviews.MainMain.as_view(), name="product-main"),
    path("list/<int:pk>/", productviews.Main.as_view(), name="product-list"),
    path("<int:pk>/", productviews.Detail.as_view(), name="product-detail"),
    path("create/", productviews.CreateView.as_view(), name="product-new"),
    path("category/<str:hierarchy>/", productviews.show_category, name="categories"),
    # re_path(r'^category/(?P<hierarchy>.+)/$', productviews.show_category, name='categories'),
    path("locale/", productviews.view_locale),
    path("insertold/", productviews.insert_from_old),
    path("insertold-hd/", productviews.insert_from_old_hd),
    path("generes/", productviews.test_category),
    path("categorize/", productviews.main_work, name="categorizer"),
    path("categorize-cats/", productviews.main_work_for_cats, name="categorizer-cats"),
    path("checkgroup/", productviews.check_group, name="checkgroup"),
    path("checkgroup-cat/", productviews.check_cat, name="checkgroup-cat"),
    path(
        "categorizeeverything/",
        productviews.categorize_bulk,
        name="categorize-everything",
    ),
    path(
        "prod-list/<int:pk>/",
        productviews.ProductListViewForJs.as_view(),
        name="product-list-js",
    ),
    path("find/", productviews.FindProductView.as_view(), name="find-product"),
    # Path for product graphql
    path(
        "graphql",
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)),
        name="vehicle-graphql",
    ),
]
