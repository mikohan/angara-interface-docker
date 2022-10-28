import math
from pprint import PrettyPrinter
from product.models.models import Category
from django.db.models import Avg, Q
from .models import Product, ProductRating

pp = PrettyPrinter(indent=2)


def ratingAvg(productId):
    try:
        product = Product.objects.get(id=productId)
        qs = ProductRating.objects.filter(product=product)
        avg = qs.aggregate(avg_score=Avg("score"))
        count = qs.count()
        ret_scor = round(avg["avg_score"], 2)

        return ret_scor, count
    except Exception as e:
        return None, None


def makeProduct(prod):

    cats = [
        {
            "id": x.id,
            "name": x.name,
            "slug": x.slug,
            "parent": x.parent.id,
        }
        for x in prod.category.all()
    ]

    breads = []
    for cat in cats:
        brad = Category.objects.get(
            id=cat["id"]).get_ancestors(include_self=True)
        some = [{"slug": x.slug, "name": x.name} for x in brad]
        breads.append(some)

    models = [
        {
            "id": x.id,
            "slug": x.slug,
            "name": x.name,
            "model": x.name,
            "priority": x.priority,
            "image": x.image.url if x.image else None,
            "rusname": x.rusname,
            "make": {
                "slug": x.carmake.slug,
                "name": x.carmake.name,
                "id": x.carmake.id,
                "country": x.carmake.country,
            },
        }
        for x in prod.car_model.all()
    ]
    engines = [
        {
            "id": x.id,
            "name": x.name,
            "image": x.image.url if x.image else None,
        }
        for x in prod.engine.all()
    ]

    images = []
    for x in prod.images.all():
        try:
            images.append(
                {
                    "img150": x.img150.url if x.img150 else None,
                    "img245": x.img245.url if x.img245 else None,
                    "img500": x.img500.url if x.img500 else None,
                    "img800": x.img800.url if x.img800 else None,
                    "img150x150": x.img150x150.url if x.img150x150 else None,
                    "img245x245": x.img245.url if x.img245x245 else None,
                    "img500x500": x.img500x500 if x.img500x500 else None,
                    "img800x800": x.img800x800 if x.img800x800 else None,
                    "main": x.main,
                    "dimension": {"width": x.img800.width, "height": x.img800.height}
                    if x.img800
                    else None,
                }
            )
        except Exception as e:
            print("Error in product images schema_helpers line 80", e)
    attrs = [
        {"name": x.attribute_name.name, "value": x.attribute_value}
        for x in prod.product_attribute.all()
    ]

    stock = {
        "id": "23",
        "store": {
            "id": 3,
            "name": "Angara",
            "location_city": "Moscow",
            "location_address": "Some address",
        },
        "price": 0,
        "quantity": 2,
        "availability_days": 0,
    }
    if prod.product_stock.all():
        stocks = [
            {
                "price": x.price,
                "quantity": x.quantity,
                "store": {"id": x.store.id, "name": x.store.name},
            }
            for x in prod.product_stock.all()
        ]
    else:
        stocks = [stock]
    related = [
        {
            "slug": x.slug,
            "name": x.name,
            "id": x.id,
            "one_c_id": x.one_c_id,
            "cat_number": x.cat_number,
            "model": [
                {
                    "id": x.id,
                    "slug": x.slug,
                    "name": x.name,
                    "model": x.name,
                    "priority": x.priority,
                    "image": x.image.url if x.image else None,
                    "rusname": x.rusname,
                    "make": {
                        "slug": x.carmake.slug,
                        "name": x.carmake.name,
                        "id": x.carmake.id,
                        "country": x.carmake.country,
                    },
                }
                for x in x.car_model.all()
            ],
            "stocks": [
                {
                    "price": x.price,
                    "quantity": x.quantity,
                    "store": {"id": x.store.id, "name": x.store.name},
                }
                for x in x.product_stock.all()
            ],
            "images": [
                {
                    "img150": x.img150.url if x.img150 else None,
                    "img245": x.img245.url if x.img245 else None,
                    "img500": x.img500.url if x.img500 else None,
                    "img800": x.img800.url if x.img800 else None,
                    "img150x150": x.img150x150.url if x.img150x150 else None,
                    "img245x245": x.img245.url if x.img245x245 else None,
                    "img500x500": x.img500x500 if x.img500x500 else None,
                    "img800x800": x.img800x800 if x.img800x800 else None,
                    "main": x.main,
                }
                for x in x.images.all()
            ],
            "brand": {x.brand.brand},
        }
        for x in prod.related.all()
    ]

    # id = ID()
    # name = String(required=True)
    # slug = String(required=True)
    # one_c_id = String(required=False)
    # cat_number = String(required=False)
    # model = List(NewCarModelType, required=False)
    # stocks = List(ProductStocksType, required=False)
    # images = List(IProductImagesType, required=False)

    returnProduct = {
        "id": prod.id,
        "slug": prod.slug,
        "name": prod.name,
        "name2": prod.name2,
        "full_name": prod.full_name,
        "one_c_id": prod.one_c_id,
        "sku": prod.sku,
        "active": prod.active,
        "uint": prod.unit,
        "cat_number": prod.cat_number,
        "oem_number": prod.oem_number,
        "partNumber": prod.partNumber,
        "brand": {
            "id": prod.brand.id,
            "slug": prod.brand.slug,
            "name": prod.brand.brand,
            "country": prod.brand.country,
            "image": prod.brand.image,
        },
        "related": related,  # [x.id for x in prod.related.all()],
        "category": cats,
        "model": models,
        "engine": engines,
        "excerpt": prod.excerpt,
        "description": prod.description,
        "created_date": prod.created_date,
        "updated_date": prod.updated_date,
        "has_photo": prod.have_photo,
        "images": images,
        "video": [x.url for x in prod.product_video.all()],
        "attributes": attrs,
        "stocks": stocks,
        "bages": prod.bages,
        "rating": ratingAvg(prod.id)[0],
        "ratingCount": ratingAvg(prod.id)[1],
        "condition": prod.condition,
        "breads": breads,
    }
    return returnProduct
