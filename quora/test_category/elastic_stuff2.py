from django.conf import settings
from django.core.mail import EmailMessage
import requests, os


def do_insert():
    headers = {"Content-Type": "application/x-ndjson"}
    working_dir = os.path.join(settings.BASE_DIR, "test_category")
    path = os.path.join(working_dir, "product_mapping.json")

    with open(path, "r", encoding="utf-8") as file_mapping:
        data_mapping = file_mapping.read()

    path_insert = os.path.join(working_dir, "product_notebook2.txt")
    file_insert = open(path_insert, "r")
    with open(path_insert, "r", encoding="utf-8") as data_insert:
        data_insert = file_insert.read()

    res_delete = requests.delete(f"http://{settings.ELASTIC_URL}/prod_all", headers=headers)
    res_mapping = requests.put(
        f"http://{settings.ELASTIC_URL}/prod_all",
        data=data_mapping.encode("utf-8"),
        headers=headers,
    )
    res_insert = requests.put(
        f"http://{settings.ELASTIC_URL}/_bulk",
        data=data_insert.encode("utf-8"),
        headers=headers,
    )
    all_res = f"Elastic index inserted. Responses are Delete index - {res_delete}, Mapping index - {res_mapping}, Insert index - {res_insert}"
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
