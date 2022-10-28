import os, math, progressbar
from quora.common_lib.logger import logger
import re
import pathlib
from bs4 import BeautifulSoup
from quora.local_settings import OAUTH_OZON, OZON_ID
from product.models import Product
from django.conf import settings
import requests, json, time
from django.core.mail import send_mail
from quora.common_lib.get_parent_category import parent_category
from product.models import CategoryOzon
from quora.common_lib.get_or_make_description import clear_description
from yandex_market.common.utils import danger_class_definder, make_brand

OZON_WAREHOUSE_ID = 22190110499000


chunk_size = 100


def make_product(product):
    def get_cat_two(product):
        cats = product.category.all()
        tmp = []
        for cat in cats:
            for inn_cat in cat.get_ancestors(include_self=True):
                tmp.append(inn_cat.id)
        cts = CategoryOzon.objects.filter(shop_cat__in=tmp)
        ret = max([x.shop_cat.id for x in cts])
        final = cts.get(shop_cat=ret)
        return final.cat_id, final.name, final.ozon_type

    image_group_id = None
    imgUrl = "https://angara77.ru"  # settings.SITE_URL
    siteUrl = "https://partshub.ru"  # settings.SITE_URL
    car_make = ""
    car_model = ""
    try:
        car_make = product.car_model.first().carmake.name.lower()
        car_model = product.car_model.first().name.lower()
        if car_make == "хендай":
            car_make = "hyundai"
    except Exception as e:
        # print("No name in product", product)
        # print(e)
        pass

    name = product.make_name

    # Making brand in utils
    # If brand not exists or
    # it is not in ozon list return No brand
    brand = make_brand(product)

    default_country = "Южная Корея"
    country = None
    try:
        country = (
            product.brand.country.upper() if product.brand.country else default_country
        )
    except Exception as e:
        # print("No counnreis found")
        country = default_country
    images = []
    primary_image = ""
    try:
        images = [f"{imgUrl}{x.img800.url}" for x in product.product_image.all()]
        if len(images):
            primary_image = images[0]
    except Exception as e:
        # print(e)
        pass
    # If we dont have category of ozon continue

    try:
        category_id, category_name, ozon_type = get_cat_two(product)
        if category_name:
            category_name = category_name.strip()
    except Exception as e:
        raise ValueError("probably not found category for this product")

    description = clear_description(product)
    payload = None
    image_group_id = product.one_c_id or ""

    price = 0
    old_price = 0
    premium_price = 0
    try:
        premium_price = float(product.product_stock.first().price)
        old_price = math.ceil(premium_price + premium_price * 0.2)
        price = math.ceil(premium_price + premium_price * 0.1)
    except Exception as e:
        pass
    # Here we skip products wit price less than 200 rubles
    #         print('Shit in price', e)
    cat_number = ""
    try:
        cat_number = product.cat_number or ""
    except:
        pass

    youtube_id = ""
    try:
        youtube_id = product.product_video.first().youtube_id
    except Exception as e:
        pass
    #         print('No Youtube id', e)

    try:
        attributes = [
            {
                "complex_id": 0,
                "id": 85,
                "values": [{"dictionary_value_id": 0, "value": brand}],
            },
            {
                "complex_id": 0,
                "id": 8205,
                "values": [{"dictionary_value_id": 0, "value": "1825"}],
            },
            {
                "complex_id": 0,
                "id": 9048,
                "values": [{"dictionary_value_id": 0, "value": name}],
            },
            {
                "complex_id": 0,
                "id": 7236,
                "values": [{"dictionary_value_id": 0, "value": cat_number}],
            },
            {
                "complex_id": 0,
                "id": 8229,
                "values": [
                    {
                        "dictionary_value_id": ozon_type,
                    }
                ],
            },
            {
                "complex_id": 0,
                "id": 4191,
                "values": [
                    {
                        "dictionary_value_id": 0,
                        "value": description,
                    }
                ],
            },
            {
                "complex_id": 0,
                "id": 9024,
                "values": [{"dictionary_value_id": 0, "value": str(product.one_c_id)}],
            },
            {
                "complex_id": 0,
                "id": 10289,
                "values": [{"value": str(product.one_c_id)}],
            },
        ]

        dang = danger_class_definder(name)
        if dang:
            attributes.append(
                {
                    "complex_id": 0,
                    "id": 9782,
                    "values": [{"dictionary_value_id": dang}],
                }
            )
        if youtube_id:
            attributes.append(
                {
                    "complex_id": 0,
                    "id": 4074,
                    "values": [{"dictionary_value_id": 0, "value": youtube_id}],
                },
            )

        payload = {
            "category_id": category_id,
            #                     "color_image": "string",
            "depth": 20,
            "dimension_unit": "cm",
            "height": 20,
            "image_group_id": str(image_group_id),
            "images": images,
            "primary_image": primary_image,
            "name": name,
            "offer_id": str(product.one_c_id),
            "old_price": str(old_price),
            "premium_price": str(premium_price),
            "price": str(price),
            "vat": "0",
            "weight": 2,
            "weight_unit": "kg",
            "width": 20,
            "attributes": attributes,
        }
    except Exception as e:
        print("Crap happened in main exception", e)
    return payload


def chunkGenerator(chunk_size):
    """
    Creating products by chanks size is given in params
    """
    # Chunk size
    n = chunk_size
    # Select products with images and prices, and price must be over 200 rubels
    # Pay attention here is the mimimum price set up
    products = (
        Product.objects.filter(product_image__img150__isnull=False)
        # .filter(product_stock__quantity__gt=0)
        .filter(product_stock__price__gt=300).distinct()
    )
    print("Products selected:", products.count())
    for i in range(0, products.count(), n):
        yield products[i : i + n]


def makeJsonChunks(makeItems):

    method_name = makeItems.__name__
    chunks = chunkGenerator(chunk_size)
    success = 0
    fail = 0

    for i, chunk in enumerate(chunks):
        result = []
        for product in chunk:
            try:
                result.append(makeItems(product))
                success += 1
            except Exception as e:
                fail += 1
        if method_name == "make_product":
            logger(
                json.dumps({"items": result}, indent=2),
                f"{i}-{method_name}-chunk.json",
                "ozon",
            )
        elif method_name == "make_stock":
            logger(
                json.dumps({"stocks": result}, indent=2),
                f"{i}-{method_name}-chunk.json",
                "ozon",
            )
        if method_name == "make_product":
            yield {"items": result}
        elif method_name == "make_stock":
            yield {"stocks": result}

    print("Success:", success, "Fail:", fail)


def test():
    res = next(makeJsonChunks(make_product))


def updateProducts(chunk):
    url = f"https://api-seller.ozon.ru/v2/product/import"

    headers = {
        "Client-Id": str(OZON_ID),
        "Api-Key": str(OAUTH_OZON),
        "Content-Type": "application/json",
    }

    r = requests.post(url, data=json.dumps(chunk), headers=headers)
    return r.status_code, r.json()


def do_all_update_products(production=False, iterations=2):
    """
    production=False  -- Pass True for real request to server
    iterations=2 -- if set 0 do till the end
    send request to server but printing results in BASE_DIR/logs/ozon/
    """
    chunkGen = makeJsonChunks(make_product)
    all_responses = []
    for i, chunk in enumerate(chunkGen):
        print("Chunk Size is:", len(chunk["items"]))
        if not iterations == 0:
            if i == iterations:
                break
        if production:
            status_code, response = updateProducts(chunk)
            all_responses.append(f"{response}")
            print(f"{i} chunk here", response)
        time.sleep(5)
    try:
        send_mail(
            "Товары на OZON обновились",
            f"Скрипт, angara77.ru django/products/syncronizators/yandex_market_update.py который обновляет или добавляет товары обновился статус коды\
            и количество чанков {json.dumps(all_responses)}",
            settings.FROM_EMAIL_ADMIN,
            settings.EMAIL_ADMINS,
            fail_silently=False,
        )
    except Exception as e:
        print(e)
    print(all_responses)


def make_stock(product):
    stock = 0
    try:
        stock = 0  # product.product_stock.first().quantity
    except:
        stock = 0
    one_c_id = str(product.one_c_id)

    stock = {"offer_id": one_c_id, "stock": stock, "warehouse_id": OZON_WAREHOUSE_ID}
    return stock


def stock_request_perform(chunk):
    url = f"https://api-seller.ozon.ru/v2/products/stocks"

    headers = {
        "Client-Id": str(OZON_ID),
        "Api-Key": str(OAUTH_OZON),
        "Content-Type": "application/json",
    }

    r = requests.post(url, data=json.dumps(chunk), headers=headers)
    return r.status_code, r.json()


def stocks_update(production=False, iterations=2):

    chunkGen = makeJsonChunks(make_stock)
    all_responses = []
    for i, chunk in enumerate(chunkGen):
        print("Chunk Size is:", chunk_size)
        if not iterations == 0:
            if i == iterations:
                break
        if production:
            status_code, response = stock_request_perform(chunk)
            all_responses.append("Dumny change it later")
            print(f"{i} chunk here")
        time.sleep(5)
    try:
        send_mail(
            "Остатки на OZON обновились",
            f"Скрипт, angara77.ru django/products/syncronizators/yandex_market_update.py который обновляет или добавляет товары обновился статус коды\
            и количество чанков {json.dumps(all_responses)}",
            settings.FROM_EMAIL_ADMIN,
            settings.EMAIL_ADMINS,
            fail_silently=False,
        )
    except Exception as e:
        print(e)
    print(all_responses)
