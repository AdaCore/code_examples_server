# The manage.py command to enter examples in the database.
# This is meant to be used by the administrators of the project only.
import glob
import os
import shutil
import subprocess
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
        
        parser.add_argument('--conf', nargs=1, type=str,
                            help='parse yaml file and clone repos and add examples')

    def handle(self, *args, **options):
        
        def add_directory(d):
            # For now, consider all files in the directory to be part of the
            # example

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
                        main=metadata.get('main', ''),
                        name=metadata['name'])
            e.save()
            e.resources.add(*resources)
            
        if options.get('remove_all', False):
            # Remove all examples from the database
            Resource.objects.all().delete()
            Example.objects.all().delete()

        if options.get('dir', None):
            d = os.path.abspath(options.get('dir')[0])
            if not os.path.isdir(d):
                print "{} is not a valid directory".format(d)
                return
            add_directory(d)
            
        if options.get('conf', None):
            conffile = os.path.abspath(options.get('conf')[0])
            if not os.path.isfile(conffile):
                print "{} is not a valid configuration file".format(conffile)
                return
            
            with open(conffile, 'r') as f:
                conf = yaml.safe_load(f);
                
            for source in conf["sources"]:
                if os.path.isdir(os.path.join("resources", source["repo"])):
                    for example in source["examples"]:
                        add_directory(os.path.abspath(os.path.join("resources", source["repo"], example)))
                else:
                    dest_dir = os.path.splitext(os.path.basename(source["repo"]))[0]
                    dest_dir = os.path.join("resources", dest_dir)
                    
                    if os.path.isdir(dest_dir):
                        shutil.rmtree(dest_dir)
                    if subprocess.call(["git", "clone", source["repo"], dest_dir]) != 0:
                        print "Error cloning repo {}".format(source["repo"])
                        return
                    for example in source["examples"]:
                        add_directory(os.path.abspath(os.path.join(dest_dir, example)))
                    
