#!/bin/sh
curl -H 'Content-Type: application/x-ndjson' -XDELETE 'http://localhost:9200/prod_all';
curl -H 'Content-Type: application/x-ndjson' -XPUT \
  'http://localhost:9200/prod_all' --data-binary @/home/manhee/Projects/quora/quora/test_category/product_mapping.json;
curl -H 'Content-Type: application/x-ndjson' -XPUT \
  'http://localhost:9200/_bulk' --data-binary @/home/manhee/Projects/quora/quora/test_category/product_notebook2.txt > el_log.log;
