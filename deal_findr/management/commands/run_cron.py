from django.core.management.base import BaseCommand
from clock import clock_fun


class Command(BaseCommand):
    help = 'Run clock scheduled function'

    def handle(self, *args, **kwargs):
    	clock_fun()
        