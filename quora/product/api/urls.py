from django.urls import path, include, re_path
from product.api import views as productApiViews
from product.api import views_site as sitetApiViews
from rest_framework.routers import DefaultRouter
from product.api import views_react as RedApiViews
from .views import (
    ImageViewSet,
    VideoViewSet,
    DescriptionViewSet,
    ProductAttributeViewSet,
    ProductAttributeList,
)
from product.api import views_a77
from product.api.views_elastic_v1 import send_json
from product.api.views_elastic_search_api import (
    autocomplete,
    findNumbers,
    send_json as search_api,
)
from product.api.views_elastic_for_angara import (
    get_products_for_yandex_market_xml,
    send_json as jsontest_angara,
    get_all_cars,
    get_products_for_angara_procenka,
)
from product.api.views_elastic_v2 import send_json as send_json2
from product.api.views_elastic_related_api import similar, latest, byTag, byCarCount

router = DefaultRouter()
router.register(r"images", ImageViewSet)
router.register(r"videos", VideoViewSet)
router.register(r"description", DescriptionViewSet)
router.register(r"attribute", ProductAttributeViewSet)
router.register(r"attributes", ProductAttributeList)

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index1.html')),
    # Prefix in browser api/product/
    path(
        "product-sitemap-list/",
        views_a77.ProductSitemapView.as_view(),
        name="product-sitemap-view",
    ),
    path(
        "get-home-page-features/<str:slug>/",
        views_a77.HomePageFeaturesView.as_view(),
        name="get-home-page-features",
    ),
    path(
        "get-redirect-product-by-one-c-id/<int:one_c_id>/",
        views_a77.GetProductByOneCId.as_view(),
        name="get-redirect-product-by-one-c-id",
    ),
    path(
        "get-redirect-product-by-cat-number/<str:cat_number>/",
        views_a77.GetProductByCatNumber.as_view(),
        name="get-redirect-product-by-cat-number",
    ),
    path(
        "get-products-by-numbers/",
        views_a77.GetProductsByCatNumbers.as_view(),
        name="get-products-by-numbers",
    ),
    path(
        "get-product-by-slug/<str:slug>/",
        views_a77.GetProductBySlugView.as_view(),
        name="get-product-bu-slug-a77",
    ),
    path("", include(router.urls)),
    path(
        "get-all-categories-flat/",
        sitetApiViews.GetAllCategoriesFlat.as_view(),
        name="get-all-categories-flat",
    ),
    path(
        "detail/<int:pk>/",
        productApiViews.DetailGet.as_view(),
        name="api-product-detail",
    ),
    path(
        "related/<int:pk>/",
        productApiViews.ProductRelatedGetPutDelete.as_view(),
        name="api-product-related",
    ),
    path("list/", productApiViews.ProductList.as_view(), name="api-product-list"),
    path(
        "detailcreate/",
        productApiViews.CreateNewProduct.as_view(),
        name="create-new-product",
    ),
    path(
        "selectlistunits/",
        productApiViews.SelectFieldsUnitsView.as_view(),
        name="api-select-unit-list",
    ),
    path(
        "selectlistbrands/",
        productApiViews.SelectFieldsBrandsView.as_view(),
        name="api-select-brand-list",
    ),
    path(
        "selectlistcarmodel/<int:pk>/",
        productApiViews.SelectFieldsModelsView.as_view(),
        name="api-select-carmodel-list",
    ),
    path(
        "selectpartcarmodel/",
        productApiViews.getPartCarModel.as_view(),
        name="api-select-carmodel-one",
    ),
    path(
        "selectpartcarengine/",
        productApiViews.getPartCarEngine.as_view(),
        name="api-select-carengine-one",
    ),
    path(
        "selectlistcarmodelnew/",
        productApiViews.SelectNewProductModelsView.as_view(),
        name="api-select-carmodel-new-list",
    ),
    path(
        "selectlistcarengine/",
        productApiViews.SelectFieldsEnginesView.as_view(),
        name="api-select-carengine-list",
    ),
    path("session/", productApiViews.SetSession.as_view(), name="set-session"),
    #     path('mainimage/<int:pk>/',
    #          productApiViews.ImageMainSet.as_view(), name='main-image'),
    # front end site starts here,
    path(
        "categorytree/",
        sitetApiViews.CategoriesTreeList.as_view(),
        name="category-tree-serializer",
    ),
    path(
        "categoryfirst/",
        sitetApiViews.CategoriesListFirstLevel.as_view(),
        name="category-first-serializer",
    ),
    path("mptt-test/", sitetApiViews.MpttTest.as_view(), name="mptt-test-serializer"),
    path(
        "singleproduct/<int:pk>/",
        sitetApiViews.SingleProduct.as_view(),
        name="single-product-retrive",
    ),
    path(
        "onec/<int:pk>/",
        sitetApiViews.SingleProductC.as_view(),
        name="single-product-retrivec",
    ),
    path(
        "getcarmodelsite/<int:pk>/",
        sitetApiViews.GetCarModel.as_view(),
        name="get-car-model-site",
    ),
    path(
        "getcarmodelsiteall/",
        sitetApiViews.GetCarModelList.as_view(),
        name="get-car-model-list-site",
    ),
    path(
        "getcarmakes/",
        sitetApiViews.GetCarMakes.as_view(),
        name="get-car-makes-list-site",
    ),
    path(
        "analogs/<int:pk>/",
        sitetApiViews.ProductAnalogList.as_view(),
        name="get-analogs",
    ),
    path(
        "relatedsite/<int:pk>/",
        sitetApiViews.ProductRelatedListView.as_view(),
        name="get-relatedsite",
    ),
    # Here starts urls for RedParts site
    # Namespase starts with red
    path(
        "red/singleproduct/<slug:slug>/",
        RedApiViews.RedSingleProductAPI.as_view(),
        name="red-single-product-retrive",
    ),
    ### Starts urls for a77
    path("a77categories/", views_a77.CategoriesView.as_view(), name="cat-test"),
    ### Path for select category by slug for a77
    path(
        "a77category/<slug:slug>/",
        views_a77.SingleCategorySlugView.as_view(),
        name="cat-test-slug",
    ),
    path(
        "merchant/",
        productApiViews.SelectAllProductsVasyaView.as_view(),
        name="merchant-api",
    ),
    path(
        "jsontest-a77-yandex-markety-xml",
        get_products_for_yandex_market_xml,
        name="send_json",
    ),
    path("jsontest", send_json, name="send_json"),
    path("jsontest_v2", send_json2, name="send_json2"),
    path("jsontest-angara77", jsontest_angara, name="send_json_angara77"),
    path("jsontest-angara77-all-cars", get_all_cars, name="get_all_cars"),
    path(
        "jsontest-get-products-for-angara-procenka/<str:search>/",
        get_products_for_angara_procenka,
        name="get-products-for-angara-procenka",
    ),
    path("searchapi", search_api, name="searchapi"),
    path("autocomplete", autocomplete, name="autocomplete"),
    path("findnumber", findNumbers, name="findNumbers"),
    path("similar", similar, name="similar"),
    path("latest", latest, name="latest"),
    path("bytag", byTag, name="bytag"),
    path("by-car-count-cat", byCarCount, name="by-car-count-cat"),
]
