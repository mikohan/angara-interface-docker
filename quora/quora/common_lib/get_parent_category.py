def parent_category(product):
    """
    Method for getting root category for parts
    used in yandex.xml and yandex_market api
    """
    cats = product.category.first()
    tree = cats.get_ancestors(include_self=False)
    lst = [x.name for x in tree]
    return lst[1] or None
