# The manage.py command to enter examples in the database.
# This is meant to be used by the administrators of the project only.
import glob
import os
import yaml
from django.core.management.base import BaseCommand

from compile_server.app.models import Resource, Example

included_extensions = ['.ads', '.adb']
# The extensions for the files that we want to show in the examples


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--remove_all', const=True, default=False,
                            action='store_const',
                            help='remove all examples from the database')

        parser.add_argument('--dir', nargs=1, type=str,
                            help='add the example found in the given dir')

    def handle(self, *args, **options):

        if options.get('remove_all', False):
            # Remove all examples from the database
            Resource.objects.all().delete()
            Example.objects.all().delete()

        if options.get('dir', None):
            d = os.path.abspath(options.get('dir')[0])

            # For now, consider all files in the directory to be part of the
            # example
            if not os.path.isdir(d):
                print "{} is not a valid directory".format(d)
                return

            # Look for 'example.yaml'
            example_yaml = os.path.join(d, 'example.yaml')
            if not os.path.isfile(example_yaml):
                print 'There is no "example.yaml" in {}'.format(d)
                return

            # Check contents of example.yaml
            with open(example_yaml, 'rb') as f:
                try:
                    metadata = yaml.load(f.read())
                except:
                    print format_traceback
                    print 'Could not decode yaml in {}'.format(example_yaml)
                    return
                for field in ['name', 'description']:
                    if field not in metadata:
                        print 'example.yaml should contain a field {}'.format(
                            field)
                        return

            resources = []
            for file in glob.glob(os.path.join(d, '*')):
                if any([file.endswith(ext) for ext in included_extensions]):
                    with open(file, 'rB') as f:
                        r = Resource(basename=os.path.basename(file),
                                     contents=f.read())
                        r.save()
                        resources.append(r)

            e = Example(description=metadata['description'],
                        original_dir=d,
                        name=metadata['name'])
            e.save()
            e.resources.add(*resources)
