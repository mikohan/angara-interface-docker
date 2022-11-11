import os, json, random, re, shutil, csv
import hashlib, progressbar
from product.models import Product, Category, CarModel, ProductRating
from django.conf import settings
from django.db.models import Avg
import math
from django.utils.html import strip_tags
from bs4 import BeautifulSoup
from quora.common_lib.colors import bcolors


# try to create one big function to call


def get_stock(prod):
    # Function for getting stocks of product
    stocks = []
    for stock in prod.product_stock.all():
        stocks.append(
            {
                "price": float(stock.price),
                "quantity": stock.quantity,
                "store": {"id": stock.store.id, "name": stock.store.name},
            }
        )
    #     print(stocks)
    return stocks


def ratingAvg(productId):
    try:
        product = Product.objects.get(id=productId)
        qs = ProductRating.objects.filter(product=product).aggregate(
            avg_score=Avg("score")
        )
        return {"ratingAvg": math.ceil(qs["avg_score"])}
    except Exception as e:

        return None


def categories_work(product):

    prod_cats = []
    cats_to_return = []

    categories_last = [
        x.get_ancestors(include_self=True).all() for x in product.category.all()
    ]

    for cat in categories_last:

        for ct in cat.all():

            if ct.id not in prod_cats:
                prod_cats.append(ct.id)
                parent = None
                if hasattr(ct, "parent") and hasattr(ct.parent, "id"):
                    parent = ct.parent.id

                cats_to_return.append(
                    {
                        "id": ct.id,
                        "name": ct.name,
                        "slug": ct.slug,
                        "image": ct.image,
                        "parent": parent,
                    }
                )
    return cats_to_return


def chk_img(img):
    if img and hasattr(img, "url"):
        return img.url
    return "/some/random/string"


def file_content_cmp(new_file, old_file):
    """Function compares two files content"""

    fn = open(new_file, "r")
    n = fn.read()
    fo = open(old_file, "r")
    o = fo.read()

    hash_new = hashlib.md5(n.encode("utf8")).hexdigest()
    hash_old = hashlib.md5(o.encode("utf8")).hexdigest()
    fn.close()
    fo.close()
    return hash_new == hash_old


def getProducts():
    """Making product for inserting in file"""

    uniq_lst = []
    domain = settings.SITE_URL

    products = Product.objects.all().distinct()
    ret_index = ""
    not_returned = [
        {
            "prodOneC": 111,
            "prodName": "Dummy",
            "reason": "Doesn't have something",
        }
    ]

    print("Total products in base:", len(products))

    # with progressbar.ProgressBar(max_value=len(products_porter)) as bar:
    prodCount = 0
    for i, prod in enumerate(products):
        if prod.id in uniq_lst:
            continue
        if not prod.brand:
            not_returned.append(
                {
                    "prodOneC": prod.one_c_id,
                    "prodName": prod.name,
                    "reason": "Doesn't have brand",
                }
            )
            continue

        brand = {
            "id": prod.brand.id,
            "name": prod.brand.brand.lower(),
            "slug": prod.brand.slug,
            "original": prod.brand.original,
            "country": prod.brand.country,
            "image": chk_img(prod.brand.image),
        }
        eng_list = [
            {
                "id": x.id,
                "name": x.name.lower(),
                "image": x.image.url if x.image else None,
            }
            for x in prod.engine.all()
        ]
        model = [
            {
                "model_id": x.id,
                "name": x.name.lower(),
                "slug": x.slug,
                "priority": x.priority,
                "image": x.image.url if x.image else None,
                "make": {
                    "slug": x.carmake.slug,
                    "name": x.carmake.name.lower(),
                    "id": x.carmake.id,
                },
                "rusname": x.rusname,
            }
            for x in prod.car_model.all()
        ]

        related = [x.id for x in prod.related.all()]

        # Image stuff
        images = []
        if prod.product_image.all().exists():
            images = [
                {
                    "id": x.id,
                    "img150": domain + chk_img(x.img150),
                    "img245": domain + chk_img(x.img245),
                    "img500": domain + chk_img(x.img500),
                    "img800": domain + chk_img(x.img800),
                    "image": domain + chk_img(x.image),
                    "img245x245": domain + chk_img(x.img245x245),
                    "img500x500": domain + chk_img(x.img500x500),
                    "img800x800": domain + chk_img(x.img800x800),
                    "main": x.main,
                }
                for x in prod.images
            ]
        elif prod.old_images.all().exists():
            images = [
                {
                    "id": x.id,
                    "img150": domain + chk_img(x.img150),
                    "img245": domain + chk_img(x.img245),
                    "img500": domain + chk_img(x.img500),
                    "img800": domain + chk_img(x.img800),
                    "image": domain + chk_img(x.image),
                    "img245x245": domain + chk_img(x.img245),
                    "img500x500": domain + chk_img(x.img500),
                    "img800x800": domain + chk_img(x.img800),
                    "main": True,
                }
                for x in prod.old_images.all()
            ]

        video = [x.url for x in prod.product_video.all()]
        attributes = [
            {"name": x.attribute_name.name.lower(), "value": x.attribute_value}
            for x in prod.product_attribute.all()
        ]
        bages_choices = ["sale", "new", "hot"]
        bages = random.sample(bages_choices, 2)
        #         bages = [x.name.lower() for x in prod.bages.all()]
        stocks = get_stock(prod)  # !!! It is for real life bottom will be fake data
        # stocks = get_fake_stock(prod)
        price = (
            float(prod.product_stock.first().price)
            if prod.product_stock.exists()
            else None
        )
        name_sug = []
        name2_sug = []
        if prod.name2:
            name2_sug = [x for x in prod.name2.split(" ")]
        if prod.name:
            name_sug = [x for x in prod.name.split(" ")]
        suggesters = [prod.full_name]

        # Category working
        categories = categories_work(prod)

        description = ""
        try:
            if hasattr(prod, "product_description"):
                soup = BeautifulSoup(prod.product_description.text, "lxml")
                description = soup.get_text()
                description = re.sub("&nbsp;", " ", description, flags=re.IGNORECASE)
        except Exception as e:
            not_returned.append(
                {
                    "prodOneC": prod.one_c_id,
                    "prodName": prod.name,
                    "reason": "Doesn't have description",
                }
            )
            pass

        product_json = json.dumps(
            {
                "id": prod.id,
                "slug": prod.slug,
                "name": prod.name,
                "name2": prod.name2,
                "full_name": prod.full_name,
                "one_c_id": prod.one_c_id,
                "active": prod.active,
                "unit": None,  # prod.unit.unit_name if hasattr(prod, "unit") else "шт",
                "cat_number": prod.cat_number,
                "oem_number": prod.oem_number,
                "brand": brand,
                "breadcrumbs": "change it if it needed",
                "related": related,
                "category": categories,
                "model": model,
                "engine": eng_list,
                "excerpt": "prod.excerpt",
                "description": description,
                "rating": ratingAvg(prod.id),
                "has_photo": prod.have_photo,
                "has_photo_or_old": True if len(images) else False,
                "images": images,
                "video": video,
                "attributes": attributes,
                "stocks": stocks,
                "condition": prod.condition,
                "bages": bages,
                "reviews": "Change it when implement the logic",
                "tags": "Change this when taggs were added",
                "full_name_ngrams": prod.full_name,
                "createdDate": str(prod.created_date),
                "updatedDate": str(prod.updated_date),
                "price": price,
            }
        )
        product = f"{product_json}\n"
        index_json = json.dumps({"index": {"_index": "prod_all_test", "_id": prod.id}})
        ret_index += f"{index_json}\n" + f"{product}"
        # Adding id to uniq list for further checking
        uniq_lst.append(prod.id)
        prodCount += 1
    prodFuckedCount = len(not_returned)
    with open(os.path.join(settings.SHARED_DATA, "products_not_on_site.csv"), "w") as f:
        w = csv.DictWriter(f, not_returned[0].keys())
        w.writeheader()
        w.writerows(not_returned)

    return ret_index, prodCount, prodFuckedCount


def do_all(show_progress=False):
    """
    Getting all products regardless of cars without showing progressbar
    And making file to insert in elasticsearch
    """


def make_file_for_elastic_cron():
    new_file = os.path.join(settings.BASE_DIR, "test_category/product_notebook.txt")
    old_file = os.path.join(settings.BASE_DIR, "test_category/product_notebook2.txt")

    text_file = open(new_file, "w")
    uniq_list, prodCount, prodFuckedCount = getProducts()
    n = text_file.write(uniq_list)
    text_file.close()
    message = f"Products are maked for Elastic insert: {prodCount}\n"
    message += f"Products are fucked up: {prodFuckedCount}\n"

    if file_content_cmp(new_file, old_file):
        print("Files are the same")
    else:
        print("Files are not the same")
        shutil.copy2(new_file, old_file)
    return message
