from product.models import Product, ProductRating
import random


def insert_rating():
    products = Product.objects.all()
    count = 0
    fuck = 0
    for product in products:
        if product.product_rating.count() == 0:

            rating = ProductRating(
                product=product,
                score=random.randint(3, 5),
                quantity=random.randint(1, 20),
            )
            rating.save()
            fuck += 1

        count += 1
    print(count, fuck)
