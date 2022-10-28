import os, json, random, re
import progressbar
from product.models import Product, Category, CarModel, ProductRating
from django.conf import settings
from django.db.models import Avg
import math
from django.utils.html import strip_tags
from bs4 import BeautifulSoup

# try to create one big function to call
def do_all():

    domain = settings.SITE_URL

    # Fake stocks !!!! replace for production
    def get_fake_stock(prod):
        stocks = []

        stocks.append(
            {
                "price": round(random.random() * 10000),
                "quantity": round(random.random() * 10),
                "store": {"id": 3, "name": "Angara Main"},
            }
        )
        return stocks

    # Function for getting stocks of product
    def get_stock(prod):
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

    # For extracting categories trees
    prod = Product.objects.all()

    lst = []

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

    # Make a function for working with categories
    def getProducts(carId, uniq_lst):

        products_porter = Product.objects.filter(car_model=carId).distinct()

        for prod in products_porter:
            if prod.id in uniq_lst:
                continue
            if not prod.brand:

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
            images = [
                {
                    "id": x.id,
                    "img150": domain + chk_img(x.img150),
                    "img245": domain + chk_img(x.img245),
                    "img500": domain + chk_img(x.img500),
                    "img800": domain + chk_img(x.img800),
                    "img245x245": domain + chk_img(x.img245x245),
                    "img500x500": domain + chk_img(x.img500x500),
                    "img800x800": domain + chk_img(x.img800x800),
                    "main": x.main,
                }
                for x in prod.images
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
            if hasattr(prod, "product_description"):
                soup = BeautifulSoup(prod.product_description.text, "lxml")
                description = soup.get_text()
                description = re.sub("&nbsp;", " ", description, flags=re.IGNORECASE)

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
                }
            )
            product = f"{product_json}\n"
            index_json = json.dumps(
                {"index": {"_index": "prod_notebook", "_id": prod.id}}
            )
            index = f"{index_json}\n"
            n = text_file.write(index)
            b = text_file.write(product)

            # Adding id to uniq list for further checking
            uniq_lst.append(prod.id)

        return uniq_lst

    my_file = os.path.join(settings.BASE_DIR, "test_category/product_notebook.txt")
    try:
        os.remove(my_file)
    except:
        print("The file does not exist")
    text_file = open(my_file, "w", encoding="utf-8")

    cars = CarModel.objects.all()

    with progressbar.ProgressBar(max_value=len(cars)) as bar:
        ul = []
        for i, car in enumerate(cars):
            ul = getProducts(car.id, ul)

            bar.update(i)

    print("Tota unique products are: ", len(ul))

    text_file.close()

    return len(ul)


def do_all_two():
    """
    Getting all products regardless of cars
    """
    domain = settings.SITE_URL

    # Fake stocks !!!! replace for production
    def get_fake_stock(prod):
        stocks = []

        stocks.append(
            {
                "price": round(random.random() * 10000),
                "quantity": round(random.random() * 10),
                "store": {"id": 3, "name": "Angara Main"},
            }
        )
        return stocks

    # Function for getting stocks of product
    def get_stock(prod):
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

    # For extracting categories trees
    prod = Product.objects.all()

    lst = []

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

    # Make a function for working with categories
    def getProducts():

        uniq_lst = []

        products_porter = Product.objects.all().distinct()

        print("Total products in base:", len(products_porter))

        with progressbar.ProgressBar(max_value=len(products_porter)) as bar:
            for i, prod in enumerate(products_porter):
                if prod.id in uniq_lst:
                    continue
                if not prod.brand:

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
                stocks = get_stock(
                    prod
                )  # !!! It is for real life bottom will be fake data
                # stocks = get_fake_stock(prod)
                price =float (prod.product_stock.first().price) if prod.product_stock.exists() else None 
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
                        description = re.sub(
                            "&nbsp;", " ", description, flags=re.IGNORECASE
                        )
                except Exception as e:
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
                        "price": price
                    }
                )
                product = f"{product_json}\n"
                index_json = json.dumps(
                    {"index": {"_index": "prod_all", "_id": prod.id}}
                )
                index = f"{index_json}\n"
                n = text_file.write(index)
                b = text_file.write(product)

                # Adding id to uniq list for further checking
                uniq_lst.append(prod.id)
                bar.update(i)

            return uniq_lst

    my_file = os.path.join(settings.BASE_DIR, "test_category/product_notebook2.txt")
    try:
        os.remove(my_file)
    except:
        print("The file does not exist")
    text_file = open(my_file, "w")

    prdx = getProducts()

    text_file.close()
