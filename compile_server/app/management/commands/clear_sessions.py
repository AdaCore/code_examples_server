import os

from django.core.management.base import BaseCommand
from compile_server.app.models import ProgramRun
from compile_server.app import process_handling


class Command(BaseCommand):

    def handle(self, *args, **options):
        process_handling.cleanup_old_processes()
