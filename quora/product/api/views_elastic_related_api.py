from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests
import pprint, re
from django.conf import settings
from product.utils import stemmer

pp = pprint.PrettyPrinter(indent=2)

#
# Searching for similar products by car and name of part
#
def similar(request):

    if request.method == "GET":
        q = request.GET.get("q")
        model = request.GET.get("model") or "porter2"

        """
        Check if search by make slug exists
        """

        if model and q:
            query_array = stemmer(q)

            # If query has car model and slug
            query = {
                "size": 20,
                "sort": [
                    {"has_photo": {"order": "desc"}},
                    {"stocks.price": {"order": "desc"}},
                ],
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"model.slug.keyword": model}},
                            {
                                "match": {
                                    "name": {
                                        "query": query_array[0],
                                        "analyzer": "rebuilt_russian",
                                        "fuzziness": 1,
                                        "operator": "and",
                                    }
                                }
                            },
                        ]
                    }
                },
            }
            data = json.dumps(query)

        r = requests.get(
            f"http://{settings.ELASTIC_URL}/{settings.ELASTIC_INDEX}/_search",
            headers={"Content-Type": "application/json"},
            data=data,
        )
        if r.status_code != 200:
            raise ValueError(
                f"Request cannot be proceeded Status code is: {r.status_code}"
            )
        response = r.json()

        # Cheking if aggregation exist in the query

        data = response

        return JsonResponse(data, safe=False)

    else:
        raise Exception({"Cannot poceed the request, params are suck"})


def latest(request):
    """
    Endpoint return latest by created date filtering by price range and has photos
    """
    if request.method == "GET":
        q = request.GET.get("q")
        model = request.GET.get("model")
        limit = request.GET.get("limit") or 20
        """
        Check if search by make slug exists
        """

        if q == "latest":

            # If query has car model and slug
            query = {
                "size": limit,
                "sort": [
                    {"has_photo": {"order": "desc"}},
                    {"stocks.price": {"order": "desc"}},
                ],
                "query": {
                    "bool": {
                        "must": [
                            {"exists": {"field": "images"}},
                            {"range": {"stocks.price": {"gte": 5000, "lte": 10000}}},
                        ]
                    }
                },
            }
            data = json.dumps(query)

        r = requests.get(
            f"http://{settings.ELASTIC_URL}/{settings.ELASTIC_INDEX}/_search",
            headers={"Content-Type": "application/json"},
            data=data,
        )
        if r.status_code != 200:
            raise ValueError(
                f"Request cannot be proceeded Status code is: {r.status_code}"
            )
        response = r.json()

        # Cheking if aggregation exist in the query

        data = response

        return JsonResponse(data, safe=False)

    else:
        raise Exception({"Cannot poceed the request, params are suck"})


def byTag(request):
    """
    Endpoint return latest by created date filtering by price range and has photos
    """
    if request.method == "GET":
        q = request.GET.get("q")
        limit = request.GET.get("limit") or 20
        """
        Check if search by make slug exists
        """

        if q:

            # If query has car model and slug
            query = {
                "size": limit,
                "sort": [
                    {"has_photo": {"order": "desc"}},
                    {"stocks.price": {"order": "desc"}},
                ],
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "name": {
                                        "query": q,
                                        "analyzer": "rebuilt_russian",
                                        "fuzziness": "auto",
                                        "operator": "or",
                                    }
                                }
                            },
                            # {"exists": {"field": "images"}},
                        ]
                    }
                },
            }
            data = json.dumps(query)

        r = requests.get(
            f"http://{settings.ELASTIC_URL}/{settings.ELASTIC_INDEX}/_search",
            headers={"Content-Type": "application/json"},
            data=data,
        )
        if r.status_code != 200:
            raise ValueError(
                f"Request cannot be proceeded Status code is: {r.status_code}"
            )
        response = r.json()

        # Cheking if aggregation exist in the query

        data = response

        return JsonResponse(data, safe=False)

    else:
        raise Exception({"Cannot poceed the request, params are suck"})


def byCarCount(request):
    """
    Endpoint return aggs by car and top categories
    """
    if request.method == "GET":
        query = request.GET.get("make") or "hyundai"

        # If query has car model and slug
        query = {
            "size": 0,
            "_source": ["id", "name"],
            "query": {"match": {"model.make.slug.keyword": query}},
            "aggs": {
                "cars": {
                    "terms": {"field": "model.slug.keyword", "size": 1000},
                    "aggs": {
                        "cats": {
                            "terms": {"field": "category.name.keyword", "size": 6},
                            "aggs": {
                                "cats": {
                                    "terms": {
                                        "field": "category.slug.keyword",
                                        "size": 1,
                                    }
                                }
                            },
                        }
                    },
                }
            },
        }
        data = json.dumps(query)

        r = requests.get(
            f"http://{settings.ELASTIC_URL}/{settings.ELASTIC_INDEX}/_search",
            headers={"Content-Type": "application/json"},
            data=data,
        )
        if r.status_code != 200:
            raise ValueError(
                f"Request cannot be proceeded Status code is: {r.status_code}"
            )
        response = r.json()

        # Cheking if aggregation exist in the query

        data = response

        return JsonResponse(data, safe=False)

    else:
        raise Exception({"Cannot poceed the request, params are suck"})
