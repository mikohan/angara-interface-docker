from product.syncronizators.products_sync import sync_products
from test_category.elastic_insert import make_file_for_elastic_cron
from test_category.elastic_stuff2 import do_insert
from product.syncronizators.prices_sync import update_prices
from quora.common_lib.email_sender import send_post
import time


def do_all_products():
    start_time = time.time()
    print("Start syncing products")
    try:
        sync_products()
    except Exception as e:
        send_post(
            "Error! Sync products failed!",
            f"Syncing products failed in product/syncronizators/products_sync. Errors are {e}",
        )
    print("Start making elastic base")
    try:
        make_file_for_elastic_cron()
    except Exception as e:
        send_post(
            "Error! Making file for elasticsearch failed!",
            f"Making big file for inserting in elastic failed in test_category/elastic_insert.do_insert_two. Errors are {e}",
        )

    print("Start inserting elastic base")
    try:
        do_insert()
    except Exception as e:
        send_post(
            "Error! Inserting into elasticsearch failed!",
            f"Inserting in elastic failed in test_category/elastic_stuff2. Errors are {e}",
        )
    print("Starting update prices")
    try:
        update_prices()
    except Exception as e:
        send_post(
            "Error! Inserting prices into Prise model failed!",
            f"Inserting prices in Price model failed in product.syncronizators.prices_sync. Errors are {e}",
        )
    total_time = time.time() - start_time
    send_post(
        "Success. Products and prices was synced.",
        f"Execution tim was {total_time} seconds. Everything is OK",
    )
