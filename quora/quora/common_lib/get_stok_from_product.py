def get_stock(product):
    stocks = []
    try:
        for stock in product.product_stock.all():
            stocks.append(
                {
                    "price": float(stock.price),
                    "quantity": stock.quantity,
                    "store": {"id": stock.store.id, "name": stock.store.name},
                }
            )
    except:
        return None
    return stocks
