from datetime import datetime
from django.conf import settings
from product.models import Product, CarModel, Stock, Store
from brands.models import BrandsDict
import csv, os
import hashlib
from test_category.elastic_insert import make_file_for_elastic_cron
from test_category.elastic_stuff2 import do_insert as elastic_insert
from quora.common_lib.colors import bcolors
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# comment for testing git


def sync_products():
    start = datetime.now()
    car_model_list = {
        "Sonata": ["sonata"],
        "Elantra": ["elantra"],
        "Santa Fe": ["santafe"],
        "Porter2": ["porter2"],
        "Porter": ["porter1"],
        "Istana": ["istana"],
        "Solaris": ["solaris"],
        "Bongo": ["bongo3"],
        "Starex": ["starex"],
        "Grace": ["grace"],
        "Spectra": ["spectra"],
        "Tucson": ["tukson"],
        "Accent": ["accent"],
        "HD": ["hd65", "hd72", "hd78"],
        "Rio": ["rio"],
        "COROLLA": ["corolla"],
        "Ducato": ["ducato"],
        "TRANSIT": ["tranzit"],
        "LOGAN": ["logan"],
        "L200": ["l200"],
        "Peugeot boxer": ["bokser"],
        "Sportage": ["sportage"],
        "IX35": ["ix35"],
        "Aero tawn": ["aerotaun"],
        "FOCUS": ["fokus"],
        "JUMPER": ["dzhamper"],
        "Cerato": ["serato"],
        "Besta": ["besta"],
        "Trajet": ["tradzhet"],
        "Sorento": ["sorento"],
        "Ceed": ["ceed"],
        "Terracan": ["terakan"],
        "Pregio": ["pajero"],
        "Soul": ["soul"],
        "Tourneo connect": ["tourneo-connect"],
        "Carnival": ["carnival"],
    }
    # Bring dict keys to lowercase
    lower_cars = {}
    for key, value in car_model_list.items():
        lower_cars[key.lower()] = value

    f = 0
    csv_ids = []

    with open(settings.ONE_C_PRICE, encoding="utf-8") as file:

        file_mod_timestamp = os.path.getmtime(settings.ONE_C_PRICE)

        file_dt = datetime.utcfromtimestamp(file_mod_timestamp).strftime(
            "%d.%m.%Y %H:%M"
        )
        dt_object = datetime.fromtimestamp(file_dt)
        f_date = dt_object.strftime("%d.%m.%Y %H:%M")

        reader = csv.reader(file, delimiter=";")
        csv_list = list(reader)

    csv_dict = []
    i = 0
    for product in csv_list:
        try:
            csv_ids.append(int(product[1]))
            csv_dict.append(
                {
                    "name": product[0],
                    "one_c_id": int(product[1]),
                    "brand": product[6] if product[6] else "origin",
                    "car_model": product[3].lower(),
                    "cat_number": product[4],
                    "price": float(product[5]) if product[5] else 0,
                    "quantity": int(product[8]) if product[8] else 0,
                    "availability_days": 0,
                }
            )
        except:
            i += 1

    products = Product.objects.all()
    product_id_list = [x.one_c_id for x in products]
    prod_count = len(product_id_list)
    update_list = []
    create_list = []
    obj_create_list = []
    i = 0
    j = 0
    for csv_prod in csv_dict:
        brand = None
        car_model = None
        try:
            brand = BrandsDict.objects.get(brand=csv_prod["brand"])
        except:
            pass
        #     try:
        #         car_model = CarModel.objects.get(slug=csv_prod['car_model'])
        #         car_model_list = cars[csv_prod['car_model']]
        #     except:
        #         pass

        if csv_prod["one_c_id"] in product_id_list:
            # update product herer
            i += 1
            update_list.append(csv_prod)
            django_product = Product.objects.get(one_c_id=csv_prod["one_c_id"])
            try:
                stock = Stock.objects.get(product=django_product, store=1)
                stock.price = csv_prod["price"]
                stock.quantity = csv_prod["quantity"]
                stock.save()
            except:
                new_stock = Stock(
                    product=django_product,
                    store=Store.objects.get(id=1),
                    price=csv_prod["price"],
                    quantity=csv_prod["quantity"],
                )
                new_stock.save()
        else:
            # create product here
            j += 1
            create_list.append(csv_prod)

            new_product = Product(
                name=csv_prod["name"],
                brand=brand,
                one_c_id=csv_prod["one_c_id"],
                cat_number=csv_prod["cat_number"],
            )
            new_product.save()
            try:
                for car in lower_cars[csv_prod["car_model"].lower()]:
                    try:
                        car_model = CarModel.objects.get(slug=car.lower())
                        new_product.car_model.add(car_model)
                    except:
                        f += 1
            except:
                pass
            st = Stock(
                product=new_product,
                store=Store.objects.get(id=1),
                price=csv_prod["price"],
                quantity=csv_prod["quantity"],
            )
            st.save()

    end = datetime.now()
    t = end - start
    return f"Synced {prod_count} products, in {t}", f"File data {f_date}"


# def do_all_sync_products():
#     sync_products()
#     do_all_two()
#     elastic_insert()
#     # update_prices()


def do_all_sync_products():
    print(f"{bcolors.OKBLUE}Started syncing products with 1C{bcolors.ENDC}")
    message_sync_prod, file_date = sync_products()
    print(message_sync_prod, f"File date is: {file_date}")
    print(f"{bcolors.OKBLUE}Ends syncing products with 1C{bcolors.ENDC}")
    print(f"{bcolors.WARNING}Starting making file for elastic{bcolors.ENDC}")
    # message_el_cron = make_file_for_elastic_cron()
    # print(message_el_cron)
    print(f"{bcolors.WARNING}Ends making file for elastic{bcolors.ENDC}")
    message_el = elastic_insert()
    print(message_el)

    # update_prices()


def do_all_sync_products_cron():
    print(f"Started syncing products with 1C")
    from_email = f"Django Docker Server Admin <angara99@sendinblue.com>"
    subject = ""
    headers = {
        "Content-Type": "text/plain",
        "X-Priority": "1 (Highest)",
        "X-MSMail-Priority": "High",
    }
    try:
        message_sync_prod, file_date = sync_products()
        print(f"Ends syncing products with 1C")
        print(f"Starting making file for elastic")
        message_el_cron = make_file_for_elastic_cron()
        print(f"Ends making file for elastic")
        message_el = elastic_insert()
        # Sending email to me with information
        body = message_sync_prod
        body += message_el_cron
        body += message_el
        message = {
            "sync_products": message_sync_prod,
            "elastic_make_file": message_el_cron,
            "insert_elastic": message_el,
            "file_date": file_date,
        }

        html = render_to_string("emails/elastic_insert.html", message)
        subject = "Products Updated in Django Docker"
        email = EmailMessage(
            subject,
            html,
            from_email,
            settings.EMAIL_ADMINS,
            headers=headers,
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        # update_prices()
    except Exception as e:
        message = {"error": e}
        subject = "Error at Products Updating in Django Docker"
        html = render_to_string("emails/elastic_insert_error.html", message)
        email = EmailMessage(
            subject,
            html,
            from_email,
            settings.EMAIL_ADMINS,
            headers=headers,
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        print(e)
