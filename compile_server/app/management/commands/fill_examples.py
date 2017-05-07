# The manage.py command to enter examples in the database.
# This is meant to be used by the administrators of the project only.
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--remove_all', const=True, default=False,
                             action='store_const',
                            help='remove all examples from the database')

        parser.add_argument('--dirs', nargs='+', type=str,
                            help='add the examples found in the given dirs')

    def handle(self, *args, **options):

        if 'remove_all' in

                 #where = options['add_dir']

        #if not os.path.isdir(where):
        #    print "Pass a directory to --dir"
