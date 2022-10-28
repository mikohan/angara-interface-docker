import requests
from django.core.mail import send_mail

def check():
    headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
}
    r = requests.get('https://angara77.com/category/filtr-masljanyj/', headers=headers, verify=False)
    check = r.status_code != requests.codes.ok
    if not check:

        send_mail(
            'SITE NOT WORKING',
            'Need to restart server',
            'mikohan1@gmail.com',
            ['yellkalolka@gmail.com','taviankart@gmail.com'],
            fail_silently=False,
        )
        
