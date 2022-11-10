from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from product.syncronizators.products_sync import do_all_sync_products


class Command(BaseCommand):
    help = "Syncing products from one C file into elasticsearch"

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime("%X")
        self.stdout.write(f"Start time: {time}")
        do_all_sync_products()
        self.stdout.write(f"End time {time}")
