from product.models import Product, ProductRating
from random import randrange
import progressbar


def do_rating():
    all_prods = Product.objects.all()
    with progressbar.ProgressBar(max_value=all_prods.count()) as bar:
        for i, prod in enumerate(all_prods):
            for qty in range(1, randrange(3, 14)):
                ProductRating.objects.create(product=prod, score=randrange(4, 6))
            bar.update(i)
