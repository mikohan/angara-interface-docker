import re
from django.conf import settings


def clear_description(product):
    description = settings.PRODUCT_DESCRIPTION
    if hasattr(product, "product_description"):
        try:
            description = re.sub(r"<[^>]*>", " ", product.product_description.text)
            description = re.sub(r"\s+", " ", description)
        except:
            description = settings.PRODUCT_DESCRIPTION
    return description
