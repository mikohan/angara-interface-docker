

import csv
from django.db.models import Avg, Count
from product.models import Stock
from product.models import Product, ProductAttribute
import os, progressbar



home_directory = os.path.expanduser( '~' )







def make_list_for_anton():
    stocks = Stock.objects.filter(quantity__gt=0)
    print(stocks.count())
    items = []
    def cats(cat):
        ret = ''
        try:
            ret = '|'.join([x.name for x in cat.get_family()])
        except:
            ret = ''
        return ret
            
    with open(os.path.join(home_directory, 'tmp', 'list.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"')
        writer.writerow(['one_c_id', 'name', 'make', 'model','category', 'brand', 'price', 'quantity', 'cat_number'])

        for stock in stocks:
            
            item =[ stock.product.one_c_id, stock.product.name,\
                    "|".join([x.carmake.name for x in stock.product.car_model.all()]),\
                    "|".join([x.name for x in stock.product.car_model.all()]),\
                   cats(stock.product.category.first()),\
                    str(stock.product.brand), str(stock.price), stock.quantity, \
                    stock.product.cat_number
                  ]
            #writer.writerow(item)
            items.append(item)
            writer.writerow(item)

# uniqilize attributes

def del_duplicates_in_attributes(product_id):
    attributes = ProductAttribute.objects.filter(product_id=product_id)
    attr_names = []
    for a in attributes:    
        if not a.attribute_name.name in attr_names:
            attr_names.append(a.attribute_name.name)
        else:        
            ProductAttribute.objects.get(id=a.id).delete()

def make_attributes_clean():
    
    products = Product.objects.filter(product_attribute__isnull=False)

    with progressbar.ProgressBar(max_value=products.count()) as bar:    
        for i, p in enumerate(products):
            del_duplicates_in_attributes(p.id)
            bar.update(i)

