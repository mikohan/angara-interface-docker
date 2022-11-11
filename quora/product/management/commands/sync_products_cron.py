from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import datetime
from django.conf import settings
import os
from quora.common_lib.colors import bcolors

from product.syncronizators.products_sync import do_all_sync_products_cron
from test_category.elastic_insert import make_file_for_elastic_cron


class Command(BaseCommand):
    help = "Syncing products from one C file into elasticsearch"

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime("%X")
        file_mod_timestamp = os.path.getmtime(settings.ONE_C_PRICE)

        file_dt = datetime.datetime.utcfromtimestamp(file_mod_timestamp).strftime(
            "%d.%m.%Y %H:%m"
        )
        time_end = timezone.now().strftime("%X")
        self.stdout.write(f"{bcolors.OKCYAN}Start time: {time}{bcolors.ENDC}")
        self.stdout.write(
            f"{bcolors.WARNING}Price modification time: {file_dt}{bcolors.ENDC}"
        )
        # make_file_for_elastic_cron()
        do_all_sync_products_cron()
        self.stdout.write(f"{bcolors.OKCYAN}End time {time_end}{bcolors.ENDC}")
