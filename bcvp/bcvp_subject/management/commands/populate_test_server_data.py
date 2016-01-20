from django.core.management.base import BaseCommand

from bcvp.load_edc import load_edc

from ...tests.factories import RecentInfectionFactory


class Command(BaseCommand):

    args = 'number to create'
    help = 'Create test recent infections data on a fresh DB.'

    def handle(self, *args, **options):
        load_edc()
        count = 0
        try:
            total = int(args[0])
        except ValueError:
            print 'Enter a valid integer, not "{}"'.format(args[0])
            return
        for _ in range(0, total):
            recent_infection = RecentInfectionFactory()
            count += 1
            print '{}/{} {}'.format(count, total, recent_infection)
