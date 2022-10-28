from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests
import pprint
from django.conf import settings

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


def make_query(request, aggs, aggs_size, category=False, page_from=1, page_size=200):
    query = []
    boolShould = []
    price = request.GET.get("price")
    priceMin = 1
    priceMax = 10000000
    sort_price = request.GET.get("sort_price") or "desc"

    print(request.GET.getlist('brand'))

    if price:
        spl = price.split("-")
        priceMin = spl[0]
        priceMax = spl[1]

    for item in request.GET.items():
        
        if str(item[0]) == "page_from" or str(item[0]) == "page_size":
            continue
        if item[0] == "sort_price":
            continue
        # must here
        
        second = item[1].split(",")
        if item[0] == "model" or item[0] == "category" and category:
            query.append(
                {"term": {f"{item[0]}.slug.keyword": second[0]}},
            )

        inside = []  # var for collecting inner filter values
        if str(item[0]) != "category" and str(item[0]) != "model":
            for filVal in second:
                if str(item[0]) == "price":
                    # adding range here
                    lst = {
                        "range": {"stocks.price": {"gte": priceMin, "lte": priceMax}}
                    }

                elif item[0] == "bages" or item[0] == "condition":
                    lst = {"term": {f"{item[0]}.keyword": filVal}}
                elif item[0] == "has_photo":
                    phot = "false"
                    if filVal == "0":
                        phot = "false"
                    else:
                        phot = "true"
                    lst = {"term": {"has_photo": phot}}
                elif item[0] == "car_models":
                    lst = {"term": {"model.name.keyword": filVal}}
                else:
                    lst = {"term": {f"{item[0]}.name.keyword": filVal}}
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
        page_size = request.GET.get("page_size") or 200

        page_from = request.GET.get("page_from") or 0
        search = request.GET.get("search") or None
        sort_price = request.GET.get("sort_price") or "desc"

        filters_chk = request.GET.get("filters_chk")
        cat = request.GET.get("category")
        model = request.GET.get("model")
        make = request.GET.get("make")
        data = None
        q_list = [x[0] for x in request.GET.items()]
        filters_chk = checFilters(filters_params, q_list)

        if model and not make and filters_chk:
            print("IN make models and filters")
            data = make_query(request, aggs, aggs_size, True, page_from, page_size)

        # Below is condition for category only and filters for autoparts page
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
            print("In CATEGORY statement")
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
                    "size": 10000,
                    "sort": [
                        {"has_photo": {"order": sort_price}},
                        {"stocks.price": {"order": "desc"}},
                    ],
                    "query": {"match_all": {}},
                    "aggs": aggs(aggs_size),
                }
            )
        # if query has q == all and cat slug

    r = requests.get(
        f"http://{settings.ELASTIC_URL}/{settings.ELASTIC_INDEX}/_search",
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
                    "id": new_cat.id,
                    "name": new_cat.name,
                    "parent": new_cat.parent_id,
                    "layout": new_cat.layout,
                    "type": new_cat.type,
                    "slug": new_cat.slug,
                }
            )
        response["aggregations"]["categories"]["buckets"] = rebuilt_cats

    data = response

    return JsonResponse(data, safe=False)


def send_json_filters(request):
    aggs_size = 2000
    data = None
    product_sizes = 200
    cat_slug = None
    query = None
    makeSlug = None
    if request.method == "GET":
        """
        Check if search by make slug exists
        """
        if request.GET.get("makeSlug"):

            makeSlug = request.GET.get("makeSlug")
            makeSlug = makeSlug.lower()
            data = json.dumps(
                {
                    "size": product_sizes,
                    "query": {"term": {"model.make.slug.keyword": makeSlug}},
                    "aggs": {
                        "unique_ids": {"terms": {"field": "id"}},
                        "categories": {
                            "terms": {"field": "category.id", "size": aggs_size}
                        },
                        "brands": {"terms": {"field": "brand.name.keyword"}},
                        "engines": {"terms": {"field": "engine.name.keyword"}},
                        "car_models": {"terms": {"field": "model.name.keyword"}},
                        "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                    },
                }
            )

        else:
            """
            Here starts parts if no query by makeSlug search
            """
            if request.method == "GET":
                if request.GET.get("q") == "all":
                    print(
                        "\033[93m",
                        "Attention ALL PRODUCTS REQUEST PERFORMED!",
                        request.GET,
                    )
                if "q" in request.GET:
                    query = request.GET["q"].lower()
                if "cat" in request.GET:
                    cat_slug = request.GET["cat"].lower()

            data = json.dumps(
                {
                    "size": product_sizes,
                    "query": {"match_all": {}},
                    "aggs": {
                        "unique_ids": {"terms": {"field": "id"}},
                        "categories": {
                            "terms": {"field": "category.id", "size": aggs_size}
                        },
                        "brands": {"terms": {"field": "brand.name.keyword"}},
                        "engines": {"terms": {"field": "engine.name.keyword"}},
                        "car_models": {"terms": {"field": "model.name.keyword"}},
                        "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                    },
                }
            )

            # If query has query and car model
            if query and not cat_slug:
                data = json.dumps(
                    {
                        "size": product_sizes,
                        "query": {"term": {"model.slug.keyword": query}},
                        "aggs": {
                            "unique_ids": {"terms": {"field": "id"}},
                            "categories": {
                                "terms": {"field": "category.id", "size": aggs_size}
                            },
                            "brands": {"terms": {"field": "brand.name.keyword"}},
                            "engines": {"terms": {"field": "engine.name.keyword"}},
                            "car_models": {"terms": {"field": "model.name.keyword"}},
                            "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                        },
                    }
                )
            # If query has car model and slug
            if query and cat_slug:
                data = json.dumps(
                    {
                        "size": product_sizes,
                        "query": {
                            "bool": {
                                "must": [
                                    {"term": {"model.slug.keyword": query}},
                                    {"term": {"category.slug.keyword": cat_slug}},
                                ]
                            }
                        },
                        "aggs": {
                            "unique_ids": {"terms": {"field": "id"}},
                            "categories": {
                                "terms": {"field": "category.id", "size": aggs_size}
                            },
                            "brands": {"terms": {"field": "brand.name.keyword"}},
                            "engines": {"terms": {"field": "engine.name.keyword"}},
                            "car_models": {"terms": {"field": "model.name.keyword"}},
                            "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                        },
                    }
                )

            # if query has q == 'all'
            if query == "all" and not cat_slug:
                data = json.dumps(
                    {
                        "size": product_sizes,
                        "query": {"match_all": {}},
                        "aggs": {
                            "unique_ids": {"terms": {"field": "id"}},
                            "categories": {
                                "terms": {"field": "category.id", "size": 2000}
                            },
                            "brands": {"terms": {"field": "brand.name.keyword"}},
                            "engines": {"terms": {"field": "engine.name.keyword"}},
                            "car_models": {"terms": {"field": "model.name.keyword"}},
                            "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                        },
                    }
                )
            # if query has q == all and cat slug

    r = requests.get(
        f"http://{settings.ELASTIC_URL}/{settings.ELASTIC_INDEX}/_search",
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
                    "id": new_cat.id,
                    "name": new_cat.name,
                    "parent": new_cat.parent_id,
                    "layout": new_cat.layout,
                    "type": new_cat.type,
                    "slug": new_cat.slug,
                }
            )
        response["aggregations"]["categories"]["buckets"] = rebuilt_cats

    data = response

    return JsonResponse(data, safe=False)
