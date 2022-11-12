from django.db.models.query import QuerySet
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests
import pprint, re, os, time
from django.conf import settings

pp = pprint.PrettyPrinter(indent=2)
autocomplete_size = 14
fuzziness = "1"  # "auto" # Pssible value

main_params = ["model", "category"]
filters_params = [
    "brand",
    "engine",
    "bages",
    "price",
    "image",
    "has_photo",
    "condition",
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
    search = request.GET.get("search")
    sort_price = request.GET.get("sort_price") or "desc"
    if price:
        spl = price.split("-")
        priceMin = spl[0]
        priceMax = spl[1]

    for item in request.GET.items():
        if item[0] == "sort_price":
            continue
        if str(item[0]) == "page_from" or str(item[0]) == "page_size":
            continue
        # must here
        second = item[1].split(",")
        if item[0] == "search":
            # If search is a number
            if re.match(r"^\d+", str(search)):
                search = str(search)

                if bool(re.search(r"[a-zA-Z]", search)):
                    """Checking if letter in number so it cat number otherwise it migth be a one c id"""
                    query.append(
                        {
                            "bool": {
                                "must": [
                                    {
                                        "bool": {
                                            "should": [
                                                {
                                                    "wildcard": {
                                                        "cat_number": {
                                                            "value": f"{search}*",
                                                            "case_insensitive": "true",
                                                        }
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "cat_number": {
                                                            "query": search,
                                                        }
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "oem_number": {
                                                            "query": search,
                                                        }
                                                    }
                                                },
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    )

                else:
                    """Here is if search not cntains a letter in string so it can be one c id"""
                    query.append(
                        {
                            "bool": {
                                "must": [
                                    {
                                        "bool": {
                                            "should": [
                                                {
                                                    "wildcard": {
                                                        "cat_number": {
                                                            "value": f"{search}*",
                                                            "case_insensitive": "true",
                                                        }
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "cat_number": {
                                                            "query": search,
                                                            "analyzer": "standard",
                                                        }
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "oem_number": {
                                                            "query": search,
                                                            "analyzer": "standard",
                                                        }
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "one_c_id": {
                                                            "query": search,
                                                            "analyzer": "standard",
                                                        }
                                                    }
                                                },
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    )

            else:
                # Search by full name and model

                query.append(
                    {
                        "bool": {
                            "should": [
                                {
                                    "wildcard": {
                                        "cat_number": {
                                            "value": f"{search}*",
                                            "case_insensitive": "true",
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "full_name": {
                                            "query": f"{second[0]}",
                                            "operator": "and",
                                        }
                                    }
                                },
                            ],
                        }
                    },
                )

        inside = []  # var for collecting inner filter values
        if str(item[0]) != "search":
            for filVal in second:
                if str(item[0]) == "price":
                    # adding range here
                    lst = {
                        "range": {"stocks.price": {"gte": priceMin, "lte": priceMax}}
                    }

                elif item[0] == "category" or item[0] == "condition":
                    lst = {"term": {f"{item[0]}.slug.keyword": filVal}}
                elif item[0] == "car_models":
                    lst = {"term": {"model.name.keyword": filVal}}
                elif item[0] == "condition":
                    lst = {"term": {f"{item[0]}.slug.keyword": filVal}}
                elif item[0] == "bages" or item[0] == "condition":
                    lst = {"term": {f"{item[0]}.keyword": filVal}}
                elif item[0] == "has_photo":
                    phot = "false"
                    if filVal == "0":
                        phot = "false"
                    else:
                        phot = "true"
                    lst = {"term": {"has_photo": phot}}
                else:
                    lst = {"term": {f"{item[0]}.name.keyword": filVal}}
                inside.append(lst)
            # pp.pprint(inside)

            subitem = {"bool": {"should": [x for x in inside]}}
            boolShould.append(subitem)
            pp.pprint(subitem)

    tmp = {
        "from": page_from,
        "size": page_size,
        # "sort": [
        #     {"has_photo": {"order": sort_price}},
        #     {"stocks.price": {"order": "desc"}},
        # ],
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

    with open(os.path.join(settings.BASE_DIR, "test_category/sample.json"), "w") as f:
        json.dump(tmp, f, indent=2)
    f.close()

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

        cat = request.GET.get("category")
        model = request.GET.get("model")
        make = request.GET.get("make")
        q_list = [x[0] for x in request.GET.items()]
        filters_chk = checFilters(filters_params, q_list)

        data = make_query(request, aggs, aggs_size, True, page_from, page_size)

        # If query has car model and slug

    r = requests.get(
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
            try:
                new_cat = Category.objects.get(id=category["key"])
            except Exception as e:
                print("Error in replace categories in elasticsearc", e)
                print("key does not exists: ", category["key"])
            rebuilt_cats.append(
                {
                    "id": category["key"],  # type: ignore
                    "count": category["doc_count"],  # type: ignore
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

    # time.sleep(4) #mock time delay for testing
    return JsonResponse(data, safe=False)


def autocomplete(request):
    query = None
    if request.method == "GET":
        """
        Check if search by make slug exists
        """
        q = request.GET.get("q")

        # If query has car model and slug
        # query = {"size": "20", "query": {"prefix": {"full_name": {"value": q}}}}
        query = {
            "size": autocomplete_size,
            "_source": ["id", "name"],
            "query": {
                "match": {
                    "name": {
                        "query": q,
                        "analyzer": "rebuilt_russian",
                        "fuzziness": fuzziness,
                        "operator": "and",
                    }
                }
            },
        }
        if request.GET.get("model"):

            query = {
                "size": autocomplete_size,
                "_source": ["id", "name"],
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"model.slug.keyword": "porter1"}},
                            {
                                "match": {
                                    "name": {
                                        "query": "помпа портер насос",
                                        "analyzer": "rebuilt_russian",
                                        "fuzziness": fuzziness,
                                        "operator": "and",
                                    }
                                }
                            },
                        ]
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

    data = response

    return JsonResponse(data, safe=False)


def findNumbers(request):
    if request.method == "GET":
        """
        Check if search by make slug exists
        """
        q = request.GET.get("q")
        if not q:
            q = "Dummy"

        # If query has car model and slug
        # query = {"size": "20", "query": {"prefix": {"full_name": {"value": q}}}}
    query = {
        "query": {"match": {"cat_number": {"query": q, "analyzer": "standard"}}},  # type: ignore
    }

    r = requests.get(
        settings.ELASTIC_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(query),
    )
    if r.status_code != 200:
        raise ValueError(f"Request cannot be proceeded Status code is: {r.status_code}")
    response = r.json()

    data = response

    return JsonResponse(data, safe=False)
