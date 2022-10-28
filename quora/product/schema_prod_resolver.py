from product.models import Product


def resolve_poduct(self, info, slug):

    prod = Product.objects.get(slug=slug)
    print(prod)
    cats = [
        {
            "id": x.id,
            "name": x.name,
            "slug": x.slug,
            "image": x.image.url if x.image else None,
            "parent": x.parent.id,
        }
        for x in prod.category.all()
    ]

    models = [
        {
            "id": x.id,
            "slug": x.slug,
            "name": x.name,
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
    images = [
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
        for x in prod.images.all()
    ]
    attrs = [
        {"name": x.attribute_name.name, "value": x.attribute_value}
        for x in prod.product_attribute.all()
    ]
    stocks = [
        {
            "price": x.price,
            "quantity": x.quantity,
            "store": {"id": x.store.id, "name": x.store.name},
        }
        for x in prod.product_stock.all()
    ]

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
            "name": prod.brand.name,
            "country": prod.brand.country,
            "image": prod.brand.image,
        },
        "related": [x.id for x in prod.related.all()],
        "category": cats,
        "model": models,
        "engines": engines,
        "excerpt": prod.excerpt,
        "description": prod.description,
        "created_date": prod.created_date,
        "updated_date": prod.updated_date,
        "has_photo": prod.have_photo,
        "images": images,
        "videoa": [x.url for x in prod.product_video.all()],
        "attributes": attrs,
        "stocks": stocks,
        "bages": [{"bage": x.name} for x in prod.bages.all()],
        "reviews": prod.reviews,
        "condition": prod.condition,
    }
    return returnProduct
