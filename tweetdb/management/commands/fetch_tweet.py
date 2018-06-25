from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update tweets"

    def handle(self, *args, **options):
        pass
