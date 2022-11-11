from django.conf import settings
from django.core.mail import EmailMessage
import requests, os
from quora.common_lib.colors import bcolors


def do_insert():
    """Inserting data from file into elastic search _bulk"""
    headers = {"Content-Type": "application/x-ndjson"}
    working_dir = os.path.join(settings.BASE_DIR, "test_category")
    path = os.path.join(working_dir, "product_mapping.json")

    with open(path, "r", encoding="utf-8") as file_mapping:
        data_mapping = file_mapping.read()

    path_insert = os.path.join(working_dir, "product_notebook2.txt")
    file_insert = open(path_insert, "r")
    with open(path_insert, "r", encoding="utf-8") as data_insert:
        data_insert = file_insert.read()

    res_delete = requests.delete(
        f"{settings.ELASTIC_URL_INSERT}/prod_all", headers=headers
    )
    res_mapping = requests.put(
        f"{settings.ELASTIC_URL_INSERT}/prod_all",
        data=data_mapping.encode("utf-8"),
        headers=headers,
    )
    res_insert = requests.put(
        f"{settings.ELASTIC_URL_INSERT}/_bulk",
        data=data_insert.encode("utf-8"),
        headers=headers,
    )
    all_res = f"{bcolors.WARNING}Elastic index inserted. Responses are Delete index - {res_delete}{bcolors.ENDC}\n{bcolors.OKBLUE} Mapping index - {res_mapping}{bcolors.ENDC}\n{bcolors.OKGREEN} Insert index - {res_insert}{bcolors.ENDC}"
    from_email = f"PartsHub Admin <mikohan1@gmail.com>"
    headers = {
        "Content-Type": "text/plain",
        "X-Priority": "1 (Highest)",
        "X-MSMail-Priority": "High",
    }
    email = EmailMessage(
        "Elastic index inserted",
        all_res,
        from_email,
        settings.EMAIL_ADMINS,
        headers=headers,
    )
    # email.send(fail_silently=False)
    print(all_res)
