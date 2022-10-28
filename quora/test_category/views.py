from django.shortcuts import render
from django.http import HttpResponse
from test_category.elastic_insert import do_all
from django.conf import settings
import requests, json
import os

# Create your views here.
def elastic_file_create(request):
    try:
        prods = True  # do_all()
        prods = do_all()
        return HttpResponse(f"<h1>Created {prods} Products so far</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>Somethin went wrong {e}</h1>")


# curl -H 'Content-Type: application/x-ndjson' -XDELETE 'http://{settings.ELASTIC_URL}/prod_notebook';
# curl -H 'Content-Type: application/x-ndjson' -XPUT 'http://{settings.ELASTIC_URL}/prod_notebook'
# --data-binary @/home/manhee/Projects/quora/quora/test_category/product_mapping.json;
# curl -H 'Content-Type: application/x-ndjson' -XPUT 'http://{settings.ELASTIC_URL}/_bulk' --data-binary @/home/manhee/Projects/quora/quora/test_category/product_notebook.txt > el_log.txt;
