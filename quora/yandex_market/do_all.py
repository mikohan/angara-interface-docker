from yandex_market.yandex_market_api.yandex_market_update import (
    do_all_update_prices as y_price,
)
from yandex_market.yandex_market_api.yandex_market_update import (
    do_all_update_products as y_products,
)
from yandex_market.ozon_api.ozon_update import do_all_update_products as oz_products
from yandex_market.ozon_api.ozon_update import stocks_update as oz_stock
from product.syncronizators.products_sync import do_all_sync_products_cron


def update_all_marktplaces():
    """Updates all products and elastic stuff and updates marketplaces"""

    do_all_sync_products_cron()
    y_products(True, 0)
    y_price(True)
    oz_products(True, 0)
    oz_stock(True, 0)
