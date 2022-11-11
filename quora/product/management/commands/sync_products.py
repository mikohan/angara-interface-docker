from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import datetime
from django.conf import settings
import os
from quora.common_lib.colors import bcolors

from product.syncronizators.products_sync import do_all_sync_products


class Command(BaseCommand):
    help = "Syncing products from one C file into elasticsearch"

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime("%X")
        file_mod_timestamp = os.path.getmtime(settings.ONE_C_PRICE)

        file_dt = datetime.datetime.utcfromtimestamp(file_mod_timestamp).strftime(
            "%d.%m.%Y %H:%m"
        )
        self.stdout.write(f"{bcolors.HEADER}Start time: {time}{bcolors.ENDC}")
        self.stdout.write(f"Price modification time: {file_dt}")
        do_all_sync_products()
        self.stdout.write(f"{bcolors.OKCYAN}End time {time}{bcolors.ENDC}")
