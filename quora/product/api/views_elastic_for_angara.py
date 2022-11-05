from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category, CarEngine
import json, time
import requests
import pprint
from django.conf import settings
from brands.models import BrandsDict
from product.models.models_vehicle import CarModel


pp = pprint.PrettyPrinter(indent=2)

main_params = ["model", "category"]
filters_params = [
    "brand",
    "engine",
    "bages",
    "price",
    "image",
    "has_photo",
    "condition",
    "car_models",
]


def aggs(size):
    aggs = {
        "categories": {"terms": {"field": "category.id", "size": size}},
        "brands": {"terms": {"field": "brand.name.keyword"}},
        "engines": {"terms": {"field": "engine.name.keyword"}},
        "car_models": {"terms": {"field": "model.name.keyword"}},
        "bages": {"terms": {"field": "bages.keyword", "size": 5}},
        "condition": {"terms": {"field": "condition.keyword", "size": 5}},
        "min_price": {"min": {"field": "stocks.price"}},
        "max_price": {"max": {"field": "stocks.price"}},
        "has_photo": {"terms": {"field": "has_photo"}},
    }
    return aggs


def make_query(request, aggs, aggs_size, category=False, page_from=1, page_size=100):
    query = []
    boolShould = []
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    priceMin = 1
    priceMax = 10000000
    sort_price = request.GET.get("sort_price") or "desc"

    for key, values in request.GET.lists():
        print(key, values)

    if min_price:
        priceMin = int(min_price)
    if max_price:
        priceMax = int(max_price)

    for key, values in request.GET.lists():

        if str(key) == "page_from" or str(key) == "page_size":
            continue
        if key == "sort_price":
            continue
        # must here
        second = values
        if key == "model" or key == "category" and category:
            query.append(
                {"term": {f"{key}.slug.keyword": second[0]}},
            )

        inside = []  # var for collecting inner filter values
        if str(key) != "category" and str(key) != "model":

            for filVal in second:
                if str(key) == "price":
                    # adding range here
                    lst = {
                        "range": {"stocks.price": {"gte": priceMin, "lte": priceMax}}
                    }

                elif key == "bages" or key == "condition":
                    lst = {"term": {f"{key}.keyword": filVal}}
                elif key == "has_photo":
                    phot = "false"
                    if filVal == "0":
                        phot = "false"
                    else:
                        phot = "true"
                    lst = {"term": {"has_photo": phot}}
                elif key == "car_models":
                    lst = {"term": {"model.name.keyword": filVal}}
                else:
                    lst = {"term": {f"{key}.name.keyword": filVal}}
                inside.append(lst)
            # pp.pprint(inside)

            subitem = {"bool": {"should": [x for x in inside]}}
            boolShould.append(subitem)
            # pp.pprint(subitem)

    tmp = {
        "from": page_from,
        "size": page_size,
        "sort": [{"stocks.price": {"order": sort_price}}],
        "query": {
            "bool": {
                "must": [
                    *query,
                    {"bool": {"must": boolShould}},
                ]
            }
        },
        "aggs": aggs(aggs_size),
    }

    # pp.pprint(tmp)

    return json.dumps(tmp)


# Function for checking if filters in defined list exists in qyery params
def checFilters(filters, get):
    flag = False

    for item in get:
        if item in filters:
            flag = True
            break
    return flag


def send_json(request):
    aggs_size = 2000
    data = None
    if request.method == "GET":

        """
        Check if search by make slug exists
        """
        page_size = request.GET.get("page_size") or 100

        page_from = request.GET.get("page_from") or 0
        search = request.GET.get("search") or None
        sort_price = request.GET.get("sort_price") or "desc"

        filters_chk = request.GET.get("filters_chk")
        cat = request.GET.get("category")
        model = request.GET.get("model")
        make = request.GET.get("make")
        data = None
        print("Heres me ", page_size)
        q_list = [x[0] for x in request.GET.items()]
        filters_chk = checFilters(filters_params, q_list)

        if model and not make and filters_chk:
            print("IN make models and filters")
            data = make_query(request, aggs, aggs_size, True, page_from, page_size)

        elif cat and not make and not model and filters_chk:
            print("IN cat and not make not model and filters")
            data = make_query(request, aggs, aggs_size, True, page_from, page_size)
        # If query has car model and slug
        elif model and cat and not make:
            print("In model and cat NOT filters")
            data = json.dumps(
                {
                    "from": page_from,
                    "size": page_size,
                    "sort": [
                        {"has_photo": {"order": sort_price}},
                        {"stocks.price": {"order": "desc"}},
                    ],
                    "query": {
                        "bool": {
                            "must": [
                                {"term": {"model.slug.keyword": model}},
                                {"term": {"category.slug.keyword": cat}},
                            ]
                        }
                    },
                    "aggs": aggs(aggs_size),
                }
            )

        # For model only request comment out for now
        elif model and model != "all" and not cat and not make and not filters_chk:
            print("In model Only not working somehow")
            data = json.dumps(
                {
                    "from": page_from,
                    "size": page_size,
                    "sort": [
                        {"has_photo": {"order": sort_price}},
                        {"stocks.price": {"order": "desc"}},
                    ],
                    "query": {"term": {"model.slug.keyword": model}},
                    "aggs": aggs(aggs_size),
                }
            )

        # For make only request
        elif make and not model and not cat:
            print("in make not model not cat")

            makeSlug = make.lower()
            data = json.dumps(
                {
                    "from": page_from,
                    "size": page_size,
                    "sort": [
                        {"has_photo": {"order": sort_price}},
                        {"stocks.price": {"order": "desc"}},
                    ],
                    "query": {"term": {"model.make.slug.keyword": makeSlug}},
                    "aggs": aggs(aggs_size),
                }
            )
        # If cat and not models
        elif cat and not model and not make:
            print("In CATEGORY statement", page_from, page_size)

            data = json.dumps(
                {
                    "from": page_from,
                    "size": page_size,
                    "sort": [
                        {"has_photo": {"order": sort_price}},
                        {"stocks.price": {"order": "desc"}},
                    ],
                    "query": {"match": {"category.slug.keyword": {"query": cat}}},
                    "aggs": aggs(aggs_size),
                }
            )
        # if query has q == 'all'
        elif model == "all" and not cat:
            print("In all statement")
            data = json.dumps(
                {
                    "from": page_from,
                    "size": page_size,
                    "sort": [
                        {"has_photo": {"order": sort_price}},
                        {"stocks.price": {"order": "desc"}},
                    ],
                    "query": {"match_all": {}},
                    "aggs": aggs(aggs_size),
                }
            )
        # if query has q == all and cat slug
    # Code to write elastic query to file for test in Kibana
    # with open("/home/manhee/tmp/query.json", "w") as outfile:
    #     try:
    #         outfile.write(data)
    #         print("Data written to file")
    #     except:
    #         print("File not writes")

    r = requests.post(
        settings.ELASTIC_URL,
        headers={"Content-Type": "application/json"},
        data=data,
    )

    if r.status_code != 200:
        raise ValueError(f"Request cannot be proceeded Status code is: {r.status_code}")
    response = r.json()

    # Cheking if aggregation exist in the query
    if "aggregations" in response:
        categories = response["aggregations"]["categories"]["buckets"]
        rebuilt_cats = []
        for category in categories:
            new_cat = None
            try:
                new_cat = Category.objects.get(id=category["key"])
            except Exception as e:
                print("Error in replace categories in elasticsearc", e)
                print("key does not exists: ", category["key"])
            rebuilt_cats.append(
                {
                    "id": category["key"],
                    "count": category["doc_count"],
                    "id": new_cat.id,  # type: ignore
                    "name": new_cat.name,  # type: ignore
                    "parent": new_cat.parent_id,  # type: ignore
                    "layout": new_cat.layout,  # type: ignore
                    "type": new_cat.type,  # type: ignore
                    "slug": new_cat.slug,  # type: ignore
                }
            )
        response["aggregations"]["categories"]["buckets"] = rebuilt_cats

    data = response

    return JsonResponse(data, safe=False)


def get_all_cars(request):

    query = {
        "size": "0",
        "query": {"match_all": {}},
        "aggs": {
            "car": {
                "terms": {"field": "model.model_id", "size": 100},
                "aggs": {
                    "categories": {"terms": {"field": "category.id", "size": 2000}},
                    "brands": {"terms": {"field": "brand.id", "size": 20}},
                    "engines": {"terms": {"field": "engine.id"}},
                    "has_photo": {"terms": {"field": "has_photo"}},
                },
            }
        },
    }

    r = requests.get(
        settings.ELASTIC_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(query),
    )

    if r.status_code != 200:
        raise ValueError(f"Request cannot be proceeded Status code is: {r.status_code}")

    response = r.json()
    start = time.time()

    new_cars = []

    for cars in response["aggregations"]["car"]["buckets"]:
        brands = []
        engines = []
        categories = []
        has_photo = []
        car = CarModel.objects.get(id=cars["key"])

        cat_ids = [
            {"id": x["key"], "doc_count": x["doc_count"]}
            for x in cars["categories"]["buckets"]
        ]

        # New categories
        for cat_id in cat_ids:
            cat = Category.objects.get(id=cat_id["id"])
            categories.append(
                {
                    "id": cat.id,
                    "doc_count": cat_id["doc_count"],
                    "name": cat.name,
                    "slug": cat.slug,
                    "cat_image": cat.image.url if cat.cat_image else None,
                    "level": cat.level,
                    "parent": cat.parent.id if cat.parent else None,
                }
            )

        # New brands
        brand_ids = [
            {"id": x["key"], "doc_count": x["doc_count"]}
            for x in cars["brands"]["buckets"]
        ]
        for brand_id in brand_ids:
            brand = BrandsDict.objects.get(id=brand_id["id"])
            brands.append(
                {
                    "id": brand_id["id"],
                    "name": brand.brand,
                    "slug": brand.slug,
                    "country": brand.country,
                }
            )

        # Engine stuff
        engines_ids = [
            {"id": x["key"], "doc_count": x["doc_count"]}
            for x in cars["engines"]["buckets"]
        ]
        for engine_id in engines_ids:
            engine = CarEngine.objects.get(id=engine_id["id"])
            engines.append(
                {"id": engine_id["id"], "name": engine.name, "slug": engine.slug}
            )
        # has_photo
        has_photo_ids = [
            {"key": x["key"], "doc_count": x["doc_count"]}
            for x in cars["has_photo"]["buckets"]
        ]
        for has_photo_id in has_photo_ids:
            has_photo.append(
                {"key": has_photo_id["key"], "doc_count": has_photo_id["doc_count"]}
            )

        # Creating new cars for return
        carmake = {
            "id": car.carmake.id,
            "name": car.carmake.name,
            "country": car.carmake.country.country,
            "rusname": car.carmake.rusname,
            "priority": car.carmake.priority,
            "image": car.carmake.image.url if car.carmake.image else None,
            "slug": car.carmake.slug,
        }
        new_cars.append(
            {
                "id": car.id,
                "name": car.name,
                "slug": car.slug,
                "priority": car.priority if car.priority else 0,
                "weight": car.weight,
                "year_from": car.year_from,
                "year_to": car.year_to,
                "active": car.active,
                "image": settings.SITE_URL + car.image.url if car.image else None,
                "model_hostory": car.model_history,
                "model_liquids": car.model_liquids,
                "model_to": car.model_to,
                "make": carmake,
                "doc_count": cars["doc_count"],
                "categories": categories,
                "brands": brands,
                "engines": engines,
                "has_photo": has_photo,
            }
        )
    # print(cars)
    end = time.time()
    print("Ecexution time is", end - start)

    return JsonResponse(new_cars, safe=False)


def get_products_for_yandex_market_xml(request):

    data = json.dumps(
        {
            "size": 10000,
            "_source": [
                "one_c_id",
                "cat_number",
                "slug",
                "name",
                "name2",
                "model.name",
                "model.make.name",
                "has_photo_or_old",
                "price",
                "category.name",
                "category.id",
                "category.parent",
                "images.image",
                "brand.name",
                "cat_number",
                "description",
                "stocks",
            ],
            "query": {
                "bool": {
                    "must": [
                        {"match": {"has_photo_or_old": "true"}},
                        {"exists": {"field": "price"}},
                    ]
                }
            },
        }
    )

    r = requests.get(
        settings.ELASTIC_URL,
        headers={"Content-Type": "application/json"},
        data=data,
    )

    if r.status_code != 200:
        raise ValueError(f"Request cannot be proceeded Status code is: {r.status_code}")
    response = r.json()
    return JsonResponse(response, safe=False)


def get_products_for_angara_procenka(request, search):

    data = {
        "size": 10000,
        "_source": [
            "one_c_id",
            "cat_number",
            "slug",
            "name",
            "model.name",
            "model.make.name",
            "has_photo_or_old",
            "price",
            "category.name",
            "category.id",
            "category.parent",
            "images.image",
            "brand.name",
            "cat_number",
            "description",
            "stocks",
        ],
        "query": {
            "wildcard": {
                "cat_number": {
                    "value": f"{search}*",
                    "boost": 1.0,
                    "rewrite": "constant_score",
                }
            }
        },
    }
    # data = {"query": {"match_all": {}}}
    data = json.dumps(data)

    r = requests.get(
        settings.ELASTIC_URL,
        headers={"Content-Type": "application/json"},
        data=data,
    )

    if r.status_code != 200:
        raise ValueError(f"Request cannot be proceeded Status code is: {r.status_code}")
    response = r.json()
    return JsonResponse(response, safe=False)
