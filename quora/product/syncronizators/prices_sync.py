import pathlib, csv, progressbar
from decimal import Decimal
from product.models import Product, Price
from collections import defaultdict


def update_prices():

    d = defaultdict(dict)

    cwd = pathlib.Path().cwd()
    file_purch = cwd / "test_category/purchase_price.csv"
    file_ret = cwd / "test_category/all.csv"
    cnt = 0
    fucked_products = []
    purch_csv = open(file_purch, "r")
    ret_csv = open(file_ret, "r")

    reader_purch = csv.reader(purch_csv, delimiter=";")
    reader_ret = csv.reader(ret_csv, delimiter=";")
    purch_list = [{"one_c_id": int(x[1]), "purchase_price": x[5]} for x in reader_purch]
    ret_list = [{"one_c_id": int(x[1]), "retail_price": x[5]} for x in reader_ret]
    purch_csv.close()
    ret_csv.close()

    for l in (ret_list, purch_list):
        for elem in l:
            d[elem["one_c_id"]].update(elem)
    res_list = list(d.values())
    # print(res_list)[:5]

    with progressbar.ProgressBar(max_value=len(res_list)) as bar:
        for i, row in enumerate(res_list):
            #         print(row)
            try:
                product = Product.objects.get(one_c_id=int(row["one_c_id"]))
                retail_price = (
                    Decimal(row["retail_price"]) if row["retail_price"] else None
                )
                purchase_price = (
                    Decimal(row["purchase_price"]) if row["purchase_price"] else None
                )
                try:
                    price = Price.objects.get(product=product)
                    price.retail_price = retail_price
                    price.purchase_price = purchase_price
                    price.save()
                except:
                    price = Price(
                        product=product,
                        retail_price=retail_price,
                        purchase_price=purchase_price,
                    )
                    price.save()

            except Exception as e:
                cnt += 1
                fucked_products.append(e)
            #             pass
            bar.update(i)
    print(fucked_products, cnt)
