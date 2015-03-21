from django.core.management.base import BaseCommand

import boto
import os

class Command(BaseCommand):
    help = 'help text'

    def handle(self, *args, **options):
        conn = boto.connect_s3()
        bucket = conn.get_bucket('practiceipa')
        keys = list(bucket.list(prefix='data/', delimiter='/'))
        os.mkdir('data')
        for key in keys:
            if not key.name.endswith('/'):
                key.get_contents_to_filename(key.name)
