# The manage.py command to enter books in the database.
# This is meant to be used by the administrators of the project only.

import os
import yaml
from django.core.management.base import BaseCommand

from compile_server.app.models import Book


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--remove_all', const=True, default=False,
                            action='store_const',
                            help='remove all books from the database')

        parser.add_argument('--dir', nargs=1, type=str,
                            help='add the book found in the given dir')

    def handle(self, *args, **options):

        if options.get('remove_all', False):
            # Remove all books from the database
            Book.objects.all().delete()

        if options.get('dir', None):
            d = os.path.abspath(options.get('dir')[0])

            # Consider directory as the book
            if not os.path.isdir(d):
                print "{} is not a valid directory".format(d)
                return

            # Look for 'chapters.yaml'
            chapters_yaml = os.path.join(d, 'info.yaml')
            if not os.path.isfile(chapters_yaml):
                print 'There is no "chapters.yaml" in {}'.format(d)
                return

            # Check contents of chapters.yaml
            with open(chapters_yaml, 'rb') as f:
                try:
                    metadata = yaml.load(f.read())
                except:
                    print format_traceback
                    print 'Could not decode yaml in {}'.format(chapters_yaml)
                    return
                for field in ['title', 'description']:
                    if field not in metadata:
                        print 'chapters.yaml should contain a field {}'.format(
                            field)
                        return

            b = Book(description=metadata['description'],
                     directory=d,
                     subpath=os.path.basename(os.path.normpath(d)),
                     title=metadata['title'],
                     author=metadata['author'])
            b.save()
