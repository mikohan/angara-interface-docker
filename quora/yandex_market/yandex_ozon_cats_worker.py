from product.models import Category, CategoryYandexMarket, CategoryOzon
from django.conf import settings
import csv, pathlib, os

"""
This functions is for update and create yandex and ozon categories
"""


def yand_cats_insert_update():
    CategoryYandexMarket.objects.all().delete()
    cwd = pathlib.Path().cwd()
    file_path = os.path.join(settings.BASE_DIR, "yandex_market/data/cats.csv")

    all_cats = Category.objects.all()
    created_count = []

    with open(file_path, "r") as r_file:
        reader = csv.reader(r_file, delimiter=",")
        for row in reader:
            yand_name = row[5].split("/")[-1]
            try:
                shop_cat_id = row[1]
                cat = all_cats.get(id=shop_cat_id)
                yand_cat, created = CategoryYandexMarket.objects.update_or_create(
                    shop_cat=cat, name=yand_name
                )

                created_count.append(created)
            except Exception as e:
                print("Something goes wrong", e)

        print("Created :", len(created_count))


def ozon_cats_insert_update():
    CategoryOzon.objects.all().delete()
    cwd = pathlib.Path().cwd()
    file_path = os.path.join(settings.BASE_DIR, "yandex_market/data/cats.csv")

    all_cats = Category.objects.all()
    created_count = []

    with open(file_path, "r") as r_file:
        reader = csv.reader(r_file, delimiter=";")
        for row in reader:
            ozon_name = row[2]
            ozon_cat_id = row[3]
            ozon_type = row[4]
            try:
                shop_cat_id = row[1]
                cat = all_cats.get(id=shop_cat_id)
                oz_cat, created = CategoryOzon.objects.update_or_create(
                    shop_cat=cat,
                    name=ozon_name,
                    cat_id=ozon_cat_id,
                    ozon_type=ozon_type,
                )

                created_count.append(created)
            except Exception as e:
                print("Something goes wrong", e)

        print("Created :", len(created_count))
